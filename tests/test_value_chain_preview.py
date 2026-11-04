"""Preview renderer is business-model-independent and unapproved by construction."""
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location("preview",ROOT/"renderers/value_chain_preview/render.py")
m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)


class ValueChainPreview(unittest.TestCase):
    def file(self,name):
        return ROOT/"tests/fixtures"/name

    def test_two_models_exactly_three_dom_pages(self):
        for name in ("value_chain_manufacturing_v01.json","value_chain_asset_service_v01.json"):
            with self.subTest(fixture=name):
                with tempfile.TemporaryDirectory() as tmp:
                    out=m.render(self.file(name),tmp)
                    html=(Path(tmp)/("value_chain_"+out["source_profile"]+".html")).read_text()
                    self.assertEqual(html.count('<section class="page">'),3)
                    self.assertIn("SYNTHETIC / CANDIDATE",html)
                    self.assertEqual(out["qa_status"],"NOT_RUN")
                    self.assertFalse(out["render_authorized_for_committee"])

    def test_all_activities_and_opportunities_present(self):
        with tempfile.TemporaryDirectory() as tmp:
            fixture=self.file("value_chain_asset_service_v01.json")
            data=json.loads(fixture.read_text())
            out=m.render(fixture,tmp)
            html=(Path(tmp)/("value_chain_"+out["source_profile"]+".html")).read_text()
            for activity in data["activities"]:
                self.assertIn(activity["label"],html)
            for opportunity in data["opportunities"]:
                self.assertIn(opportunity["baseline_no_ai"],html)

    def test_html_escape_does_not_allow_script_injection(self):
        data=json.loads(self.file("value_chain_asset_service_v01.json").read_text())
        data["activities"][0]["label"]="<script>alert('x')</script>"
        html=m.render_html(data)
        self.assertNotIn("<script>",html)
        self.assertIn("&lt;script&gt;",html)


if __name__=="__main__":
    unittest.main()
