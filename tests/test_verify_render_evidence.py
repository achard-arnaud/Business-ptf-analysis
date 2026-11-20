"""QA receipt NRT: missing evidence and altered manifest must fail."""
import importlib.util
import json
import struct
import zlib
import tempfile
import unittest
from pathlib import Path
from pypdf import PdfWriter

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


if __name__=="__main__":
    unittest.main()
