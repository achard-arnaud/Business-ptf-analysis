"""Render CI impact classifier positive/negative tests."""
import importlib.util
import unittest
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
s=importlib.util.spec_from_file_location("selector",ROOT/"scripts/ci_render_selector.py")
m=importlib.util.module_from_spec(s);s.loader.exec_module(m)


class SelectRender(unittest.TestCase):
    def test_docs_only_skips_browser(self):
        self.assertFalse(m.should_render(["README.md","docs/agent/gates.md","companies/hivest/INDEX.md"]))
    def test_empty_skips_browser(self):
        self.assertFalse(m.should_render([]))
    def test_renderer_changed(self):
        self.assertTrue(m.should_render(["renderers/value_chain_preview/render.py"]))
    def test_css_changed(self):
        self.assertTrue(m.should_render(["renderers/three_pager_exec/exec_theme.css"]))
    def test_fixture_changed(self):
        self.assertTrue(m.should_render(["tests/fixtures/exec/sphere_unverified_v0.3.json"]))
    def test_template_registry_changed(self):
        self.assertTrue(m.should_render(["templates/registry.json"]))
    def test_shared_schema_changed(self):
        self.assertTrue(m.should_render(["contracts/three-pager-exec.schema.json"]))
    def test_writer_touch_triggers(self):
        self.assertTrue(m.should_render(["scripts/prepare_artifact_receipt.py"]))
    def test_workflow_changed(self):
        self.assertTrue(m.should_render([".github/workflows/contracts.yml"]))
    def test_mix_prefer_safety(self):
        self.assertTrue(m.should_render(["docs/README.md","renderers/three_pager_exec/render2.py"]))


if __name__=="__main__":
    unittest.main()
