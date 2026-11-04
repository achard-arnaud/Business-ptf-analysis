"""QA receipt NRT: missing evidence and altered manifest must fail."""
import importlib.util
import json
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
