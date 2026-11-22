"""QA receipt NRT: missing evidence and altered manifest must fail."""
import importlib.util
import json
import struct
import zlib
import tempfile
import unittest
from pathlib import Path
from pypdf import PdfWriter
from pypdf.generic import DecodedStreamObject, DictionaryObject, NameObject

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("rendercheck",ROOT/"scripts/verify_render_evidence.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class RenderEvidenceTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.folder=Path(self.temp.name)
        pdf=PdfWriter()
        for _ in range(3):pdf.add_blank_page(width=842,height=595)
        with (self.folder/"report.pdf").open("wb") as out:pdf.write(out)
        self.qa={"pass":True,"page_count":3,"summary":{key:0 for key in m.ISSUE_KEYS}}
        (self.folder/"qa.json").write_text(json.dumps(self.qa))
        self.manifest={"render_profile":"exec","visual_qa":"LAYOUT_PASS_MANUAL_PENDING",
                       "pdf_sha256":m.sha(self.folder/"report.pdf"),"qa_sha256":m.sha(self.folder/"qa.json"),
                       "png_sha256":[]}
        (self.folder/"render_manifest.json").write_text(json.dumps(self.manifest))

    def fails(self):
        with self.assertRaises(ValueError):m.verify(self.folder,profile="exec")

    def write_png_evidence(self, filenames):
        def chunk(kind, data):
            return struct.pack(">I", len(data)) + kind + data + struct.pack(">I", zlib.crc32(kind + data))

        header = struct.pack(">IIBBBBB", 842, 595, 8, 0, 0, 0, 0)
        for shade, name in enumerate(filenames, 1):
            pixels = (b"\0" + bytes([shade]) * 842) * 595
            png = (b"\x89PNG\r\n\x1a\n" + chunk(b"IHDR", header)
                   + chunk(b"IDAT", zlib.compress(pixels)) + chunk(b"IEND", b""))
            (self.folder / name).write_bytes(png)
        self.manifest["png_sha256"] = [m.sha(self.folder / name) for name in sorted(filenames)]
        (self.folder / "render_manifest.json").write_text(json.dumps(self.manifest))

    def test_repeated_page_number_does_not_replace_missing_page(self):
        self.write_png_evidence(["report_page1.png", "report_page2.png", "other_page2.png"])
        with self.assertRaisesRegex(ValueError, "screenshots"):
            m.verify(self.folder, profile="exec")

    def test_foreign_capture_does_not_complete_page_set(self):
        self.write_png_evidence(["report_page1.png", "report_page2.png", "other_page3.png"])
        with self.assertRaisesRegex(ValueError, "screenshots"):
            m.verify(self.folder, profile="exec")

    def test_pdf_capture_set_passes_without_committee_approval(self):
        self.write_png_evidence(["report_page1.png", "report_page2.png", "report_page3.png"])
        result = m.verify(self.folder, profile="exec")
        self.assertEqual(result["status"], "AUTOMATED_LAYOUT_PASS_READER_PENDING")
        self.assertFalse(result["committee_authorized"])

    def test_additional_numbered_capture_does_not_match_pdf(self):
        names = [f"report_page{i}.png" for i in (1, 2, 3)]
        self.write_png_evidence(names)
        receipt = {"sha256": self.manifest["pdf_sha256"],
                   "publication_state": "prepared_not_published",
                   "authorization_state": "UNREVIEWED", "qa_state": "PASS"}
        (self.folder / "artifact_receipt.json").write_text(json.dumps(receipt))
        capture = (self.folder / names[-1]).read_bytes()
        (self.folder / "illustration.png").write_bytes(capture)
        for profile in ("exec", "value-chain-preview"):
            with self.subTest(profile=profile):
                self.assertEqual(m.verify(self.folder, profile=profile)["physical_pages"], 3)
                extra = self.folder / "report_page4.png"
                extra.write_bytes(capture)
                try:
                    with self.assertRaisesRegex(ValueError, "screenshots"):
                        m.verify(self.folder, profile=profile)
                finally:
                    extra.unlink()

    def test_incomplete_capture_refused_even_with_matching_hash(self):
        names = ["report_page1.png", "report_page2.png", "report_page3.png"]
        for removed_bytes in (12, 14):
            with self.subTest(removed_bytes=removed_bytes):
                self.write_png_evidence(names)
                page = self.folder / names[1]
                page.write_bytes(page.read_bytes()[:-removed_bytes])
                self.manifest["png_sha256"][1] = m.sha(page)
                (self.folder / "render_manifest.json").write_text(json.dumps(self.manifest))
                with self.assertRaisesRegex(ValueError, r"report_page2\.png: .*PNG"):
                    m.verify(self.folder, profile="exec")

    def test_missing_png_refused(self):
        self.fails()

    def test_bad_chunk_crc_refused_even_with_matching_hash(self):
        names = [f"report_page{i}.png" for i in (1, 2, 3)]
        for chunk in (b"IHDR", b"IDAT", b"IEND"):
            with self.subTest(chunk=chunk):
                self.write_png_evidence(names)
                page = self.folder / names[1]
                data = bytearray(page.read_bytes())
                offset = 8
                while True:
                    length, kind = struct.unpack_from(">I4s", data, offset)
                    if kind == chunk:
                        data[offset + 8 + length] ^= 1
                        break
                    offset += 12 + length
                page.write_bytes(data)
                self.manifest["png_sha256"][1] = m.sha(page)
                (self.folder / "render_manifest.json").write_text(json.dumps(self.manifest))
                with self.assertRaisesRegex(ValueError, rf"report_page2\.png: .*{chunk.decode()}.*CRC"):
                    m.verify(self.folder, profile="exec")

    def test_manipulated_pdf_refused(self):
        self.manifest["pdf_sha256"]="a"*64
        (self.folder/"render_manifest.json").write_text(json.dumps(self.manifest))
        self.fails()

    def test_missing_layout_category_refused(self):
        del self.qa["summary"]["small_fonts"]
        (self.folder/"qa.json").write_text(json.dumps(self.qa))
        self.manifest["qa_sha256"]=m.sha(self.folder/"qa.json")
        (self.folder/"render_manifest.json").write_text(json.dumps(self.manifest))
        self.fails()

    def test_false_pass_with_overflow_rejected(self):
        self.qa["summary"]["overflows"]=1
        (self.folder/"qa.json").write_text(json.dumps(self.qa))
        self.manifest["qa_sha256"]=m.sha(self.folder/"qa.json")
        (self.folder/"render_manifest.json").write_text(json.dumps(self.manifest))
        self.fails()

    def test_physical_page_count_rejected(self):
        pdf=PdfWriter();pdf.add_blank_page(width=842,height=595)
        with (self.folder/"report.pdf").open("wb") as out:pdf.write(out)
        self.manifest["pdf_sha256"]=m.sha(self.folder/"report.pdf")
        (self.folder/"render_manifest.json").write_text(json.dumps(self.manifest))
        self.fails()

    def write_exec_witness(self, *, html_footer=True, pdf_page=2):
        self.write_png_evidence([f"report_page{i}.png" for i in range(1, 4)])
        payload = self.folder / "payload.json"
        payload.write_text(json.dumps({
            "figures": {"value": {"value": "17"}},
            "page2": {"footer": {"body": "Required **margin**: {value} & stable."}},
        }), encoding="utf-8")
        self.manifest["payload_sha256"] = m.sha(payload)
        footer = "Required <b>margin</b>: 17 &amp; stable." if html_footer else ""
        (self.folder / "report.html").write_text(
            '<section class="page"></section><section class="page">'
            '<div class="footer-strip"><div class="footer-body">'
            + footer + '</div></div></section><section class="page"></section>',
            encoding="utf-8")
        pdf = PdfWriter()
        for i in range(1, 4):
            page = pdf.add_blank_page(width=842, height=595)
            if i == pdf_page:
                font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                                         NameObject("/Subtype"): NameObject("/Type1"),
                                         NameObject("/BaseFont"): NameObject("/Helvetica")})
                page[NameObject("/Resources")] = DictionaryObject({
                    NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
                stream = DecodedStreamObject()
                stream.set_data(b"BT /F1 12 Tf 50 50 Td (Required margin: 17 & stable.) Tj ET")
                page[NameObject("/Contents")] = pdf._add_object(stream)
        with (self.folder / "report.pdf").open("wb") as out:
            pdf.write(out)
        self.manifest["pdf_sha256"] = m.sha(self.folder / "report.pdf")
        (self.folder / "render_manifest.json").write_text(json.dumps(self.manifest))
        return payload

    def test_exec_footer_checks_both_formats_on_page_two(self):
        payload = self.write_exec_witness()
        result = m.verify(self.folder, profile="exec", exec_payload=payload)
        self.assertEqual(result["exec_footer_page2"], "PASS")
        self.assertFalse(result["committee_authorized"])

    def test_exec_footer_missing_or_on_wrong_pdf_page(self):
        for html_footer, pdf_page, output in ((False, 2, "HTML"), (True, 1, "PDF"), (True, 0, "PDF")):
            with self.subTest(output=output, pdf_page=pdf_page):
                payload = self.write_exec_witness(html_footer=html_footer, pdf_page=pdf_page)
                self.assertNotIn("exec_footer_page2", m.verify(self.folder, profile="exec"))
                with self.assertRaisesRegex(ValueError, f"{output} page 2"):
                    m.verify(self.folder, profile="exec", exec_payload=payload)

    def test_exec_footer_refuses_unbound_payload(self):
        payload = self.write_exec_witness()
        payload.write_text(payload.read_text(encoding="utf-8") + "\n", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "payload.*manifest"):
            m.verify(self.folder, profile="exec", exec_payload=payload)


if __name__=="__main__":
    unittest.main()
