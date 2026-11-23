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

    def write_exec_witness(self, *, html_footer=True, pdf_page=2, all_pages=False,
                           missing_pdf_page=None, source_lines=False, moved_pdf_source=None,
                           thesis_placement=None, thesis_pdf_page=1, thesis_prose=None,
                           prose_pdf_order=(0, 1), prose_pdf_page=1):
        self.write_png_evidence([f"report_page{i}.png" for i in range(1, 4)])
        payload = self.folder / "payload.json"
        data = {
            "figures": {"value": {"value": "17"}},
            "page2": {"footer": {"body": "Required **margin**: {value} & stable."}},
        }
        html_footers = {2: "Required <b>margin</b>: 17 &amp; stable." if html_footer else ""}
        pdf_footers = {pdf_page: b"(Required margin: 17 & stable.) Tj"}
        if all_pages:
            data["page1"] = {"footer": {"body": "Opening footer."}}
            data["page3"] = {"footer": {"body": "Closing footer."}}
            html_footers.update({1: "Opening footer.", 3: "Closing footer."})
            pdf_footers.update({1: b"(Opening footer.) Tj", 3: b"(Closing footer.) Tj"})
        pdf_footers.pop(missing_pdf_page, None)
        sources = {}
        if source_lines:
            for i in range(1, 4):
                sources[i] = f"Sources: edition {i}."
                data.setdefault(f"page{i}", {})["sources"] = sources[i]
                pdf_slot = 2 if i == moved_pdf_source else i
                pdf_footers[pdf_slot] = (pdf_footers.get(pdf_slot, b"")
                                         + f" 0 -20 Td ({sources[i]}) Tj".encode("ascii"))
        cards = ""
        if thesis_placement is not None:
            data.setdefault("page1", {})["thesis"] = {"take": "Integrate before **innovating**."}
            takeaway = "Integrate before <b>innovating</b>."
            prose_html = "Body"
            if thesis_prose is not None:
                paras = ("First **claim**.", "Second claim.")
                data["page1"]["thesis"]["paras"] = list(paras)
                prose_html = "".join('<p class="lead">' + paras[i].replace("**claim**", "<b>claim</b>")
                                     + "</p>" for i in thesis_prose)
                for i in prose_pdf_order:
                    raw = paras[i].replace("**", "")
                    pdf_footers[prose_pdf_page] = (pdf_footers.get(prose_pdf_page, b"")
                                                  + f" 0 -20 Td ({raw}) Tj".encode("ascii"))
            cards = "".join(
                '<div class="card"><h2>' + title + '</h2><div class="body">'
                + (prose_html if position == "thesis" else "Other body") + '</div>'
                '<p class="take"><b class="lbl">À retenir</b>'
                + (takeaway if thesis_placement == position else "")
                + '</p></div>'
                for position, title in (("neighbor", "Signalétique"), ("thesis", "Thèse")))
            if thesis_pdf_page is not None:
                pdf_footers[thesis_pdf_page] = (pdf_footers.get(thesis_pdf_page, b"")
                                              + b" 0 -20 Td (Integrate before innovating.) Tj")
        payload.write_text(json.dumps(data), encoding="utf-8")
        self.manifest["payload_sha256"] = m.sha(payload)
        (self.folder / "report.html").write_text(
            "".join('<section class="page">' + (cards if i == 1 else "") + '<div class="footer-strip">'
                    f'<div class="footer-body">{html_footers.get(i, "")}</div>'
                    f'</div><div class="source-line">{sources.get(i, "")}</div></section>'
                    for i in range(1, 4)),
            encoding="utf-8")
        pdf = PdfWriter()
        for i in range(1, 4):
            page = pdf.add_blank_page(width=842, height=595)
            if i in pdf_footers:
                font = DictionaryObject({NameObject("/Type"): NameObject("/Font"),
                                         NameObject("/Subtype"): NameObject("/Type1"),
                                         NameObject("/BaseFont"): NameObject("/Helvetica")})
                page[NameObject("/Resources")] = DictionaryObject({
                    NameObject("/Font"): DictionaryObject({NameObject("/F1"): font})})
                stream = DecodedStreamObject()
                stream.set_data(b"BT /F1 12 Tf 50 50 Td " + pdf_footers[i] + b" ET")
                page[NameObject("/Contents")] = pdf._add_object(stream)
        with (self.folder / "report.pdf").open("wb") as out:
            pdf.write(out)
        self.manifest["pdf_sha256"] = m.sha(self.folder / "report.pdf")
        (self.folder / "render_manifest.json").write_text(json.dumps(self.manifest))
        return payload

    def test_exec_source_line_must_be_outside_inert_template(self):
        payload = self.write_exec_witness(source_lines=True)
        html = self.folder / "report.html"
        original = html.read_text(encoding="utf-8")
        line = '<div class="source-line">Sources: edition 2.</div>'
        self.assertEqual(original.count(line), 1)
        for start, end in (("<template>", "</template>"),
                           ("<template><template></template>", "</template>")):
            with self.subTest(template=start):
                html.write_text(original.replace(line, start + line + end), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "exec HTML page 2 source line differs from payload"):
                    m.verify(self.folder, profile="exec", exec_payload=payload, exec_source_lines=True)

        # An inert page must not change active page numbering or duplicate its sources.
        inert_page = '<template><section class="page">' + line + '</section></template>'
        html.write_text(inert_page + original, encoding="utf-8")
        result = m.verify(self.folder, profile="exec", exec_payload=payload, exec_source_lines=True)
        self.assertEqual([result[f"exec_source_line_page{i}"] for i in range(1, 4)],
                         ["PASS", "PASS", "PASS"])

    def test_exec_source_line_cannot_come_only_from_script_or_style(self):
        payload = self.write_exec_witness(source_lines=True)
        html = self.folder / "report.html"
        original = html.read_text(encoding="utf-8")
        body = "Sources: edition 2."
        line = f'<div class="source-line">{body}</div>'
        self.assertEqual(original.count(line), 1)
        for opening, closing in (('<script type="text/plain">', "</script>"),
                                 ("<style>", "</style>")):
            with self.subTest(tag=opening):
                hidden = line.replace(body, opening + body + closing)
                html.write_text(original.replace(line, hidden), encoding="utf-8")
                with self.assertRaisesRegex(ValueError, "exec HTML page 2 source line differs from payload"):
                    m.verify(self.folder, profile="exec", exec_payload=payload, exec_source_lines=True)

    def test_exec_source_line_preserves_visible_text_when_raw_blocks_are_present(self):
        payload = self.write_exec_witness(source_lines=True)
        html = self.folder / "report.html"
        original = html.read_text(encoding="utf-8")
        line = '<div class="source-line">Sources: edition 2.</div>'
        self.assertEqual(original.count(line), 1)
        blocks = ('<script type="application/json">{"description":"Metadata."}</script>'
                  '<style>.commentary{color:black}</style>')
        html.write_text(original.replace(line, line.replace("edition", blocks + "edition")), encoding="utf-8")
        result = m.verify(self.folder, profile="exec", exec_payload=payload, exec_source_lines=True)
        self.assertEqual([result[f"exec_source_line_page{i}"] for i in range(1, 4)],
                         ["PASS", "PASS", "PASS"])

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

    def test_all_exec_footers_report_each_page(self):
        payload = self.write_exec_witness(all_pages=True)
        result = m.verify(self.folder, profile="exec", exec_payload=payload, all_exec_footers=True)
        self.assertEqual([result[f"exec_footer_page{i}"] for i in range(1, 4)], ["PASS"] * 3)

    def test_all_exec_footers_reject_missing_first_or_last_pdf_page_text(self):
        for i in (1, 3):
            with self.subTest(page=i):
                payload = self.write_exec_witness(all_pages=True, missing_pdf_page=i)
                self.assertEqual(m.verify(self.folder, profile="exec", exec_payload=payload)["exec_footer_page2"],
                                 "PASS")
                with self.assertRaisesRegex(ValueError, f"PDF page {i}"):
                    m.verify(self.folder, profile="exec", exec_payload=payload, all_exec_footers=True)

    def test_all_exec_footers_reject_duplicate_html_slot(self):
        payload = self.write_exec_witness(all_pages=True)
        html = self.folder / "report.html"
        footer = '<div class="footer-body">Closing footer.</div>'
        html.write_text(html.read_text(encoding="utf-8").replace(footer, 2 * footer), encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "HTML page 3"):
            m.verify(self.folder, profile="exec", exec_payload=payload, all_exec_footers=True)

    def test_source_lines_verify_all_three_pages_alongside_footers(self):
        payload = self.write_exec_witness(all_pages=True, source_lines=True)
        result = m.verify(self.folder, profile="exec", exec_payload=payload,
                          all_exec_footers=True, exec_source_lines=True)
        self.assertEqual({result[f"exec_source_line_page{i}"] for i in range(1, 4)}, {"PASS"})
        self.assertEqual(result["exec_footer_page3"], "PASS")

    def test_source_lines_reject_missing_html_text_or_pdf_text_on_wrong_page(self):
        for wrong_pdf_page in (False, True):
            with self.subTest(wrong_pdf_page=wrong_pdf_page):
                payload = self.write_exec_witness(source_lines=True,
                                                  moved_pdf_source=3 if wrong_pdf_page else None)
                html = self.folder / "report.html"
                if not wrong_pdf_page:
                    html.write_text(html.read_text(encoding="utf-8").replace("Sources: edition 3.", ""),
                                    encoding="utf-8")
                control = m.verify(self.folder, profile="exec", exec_payload=payload)
                self.assertNotIn("exec_source_line_page3", control)
                output = "PDF" if wrong_pdf_page else "HTML"
                with self.assertRaisesRegex(ValueError, f"{output} page 3 source line"):
                    m.verify(self.folder, profile="exec", exec_payload=payload, exec_source_lines=True)

    def test_thesis_takeaway_checks_its_card_and_page_alongside_existing_slots(self):
        payload = self.write_exec_witness(all_pages=True, source_lines=True, thesis_placement="thesis")
        result = m.verify(self.folder, profile="exec", exec_payload=payload, all_exec_footers=True,
                          exec_source_lines=True, exec_thesis_takeaway=True)
        self.assertEqual(result["exec_thesis_takeaway_page1"], "PASS")
        self.assertEqual(result["exec_source_line_page1"], "PASS")

    def test_thesis_takeaway_rejects_absent_or_neighboring_card_text(self):
        for placement in ("missing", "neighbor"):
            with self.subTest(placement=placement):
                payload = self.write_exec_witness(thesis_placement=placement)
                base = m.verify(self.folder, profile="exec", exec_payload=payload)
                self.assertNotIn("exec_thesis_takeaway_page1", base)
                with self.assertRaisesRegex(ValueError, "HTML page 1 thesis takeaway"):
                    m.verify(self.folder, profile="exec", exec_payload=payload, exec_thesis_takeaway=True)

    def test_thesis_takeaway_rejects_absent_or_misplaced_pdf_text(self):
        for page in (None, 2):
            with self.subTest(page=page):
                payload = self.write_exec_witness(thesis_placement="thesis", thesis_pdf_page=page)
                with self.assertRaisesRegex(ValueError, "PDF page 1 thesis takeaway"):
                    m.verify(self.folder, profile="exec", exec_payload=payload, exec_thesis_takeaway=True)

    def test_thesis_paragraphs_preserve_both_claims_in_order(self):
        payload = self.write_exec_witness(thesis_placement="thesis", thesis_prose=(0, 1))
        result = m.verify(self.folder, profile="exec", exec_payload=payload, exec_thesis_takeaway=True,
                          exec_thesis_paragraphs=True)
        self.assertEqual(result["exec_thesis_paragraphs_page1"], "PASS")
        self.assertEqual(result["exec_thesis_takeaway_page1"], "PASS")

    def test_thesis_paragraphs_reject_loss_reordering_or_wrong_pdf_page(self):
        cases = (([1], (0, 1), 1, "HTML"), ((1, 0), (0, 1), 1, "HTML"),
                 ((0, 1), (1,), 1, "PDF"), ((0, 1), (1, 0), 1, "PDF"),
                 ((0, 1), (0, 1), 2, "PDF"))
        for html_order, pdf_order, page, format_name in cases:
            with self.subTest(html=html_order, pdf=pdf_order, page=page):
                payload = self.write_exec_witness(thesis_placement="thesis", thesis_prose=html_order,
                                                  prose_pdf_order=pdf_order, prose_pdf_page=page)
                control = m.verify(self.folder, profile="exec", exec_payload=payload, exec_thesis_takeaway=True)
                self.assertNotIn("exec_thesis_paragraphs_page1", control)
                with self.assertRaisesRegex(ValueError, f"{format_name} page 1 thesis paragraphs"):
                    m.verify(self.folder, profile="exec", exec_payload=payload, exec_thesis_paragraphs=True)


if __name__=="__main__":
    unittest.main()
