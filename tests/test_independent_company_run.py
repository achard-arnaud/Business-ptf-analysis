"""End-to-end binding checks for independent company runs."""
import hashlib
import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

from pypdf import PdfReader

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "renderers" / "three_pager_exec"))
from render_exec import R  # noqa: E402
sys.path.insert(0, str(ROOT / "scripts"))
from render_independent_company_runs import bound_runs  # noqa: E402
from validate import digest  # noqa: E402

BASE = ROOT / "companies" / "square-management"


def read_json(path):
    return json.loads(path.read_text(encoding="utf-8"))


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


class IndependentCompanyRun(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.manifest = read_json(BASE / "manifest.json")
        cls.package = read_json(BASE / cls.manifest["package_ref"].removeprefix("companies/square-management/"))
        cls.graph = read_json(BASE / cls.manifest["graph_ref"].removeprefix("companies/square-management/"))
        cls.binding = read_json(BASE / "outputs/binding.json")
        cls.render_manifest = read_json(BASE / "outputs/render_manifest.json")
        cls.payload_path = BASE / "outputs/square-management-exec-payload.json"
        cls.payload = read_json(cls.payload_path)

    def test_new_company_instance_is_not_bound_to_hivest(self):
        self.assertEqual(self.manifest["entity_id"], "square-management")
        self.assertEqual(self.manifest["instance_kind"], "independent_company_analysis")
        self.assertIsNone(self.manifest["program_ref"])
        self.assertEqual(self.package["entity_id"], self.manifest["entity_id"])
        self.assertEqual(self.graph["entity_id"], self.manifest["entity_id"])
        self.assertEqual(self.payload["entity_id"], self.manifest["entity_id"])
        bundle_sha256 = digest({"package": self.package, "context": read_json(BASE / "strategic_context.json"), "graph": self.graph})
        self.assertEqual(self.payload["lineage"]["bundle_sha256"], bundle_sha256)
        self.assertEqual(self.binding["evidence_snapshot_sha256"], bundle_sha256)
        self.assertEqual(self.render_manifest["bundle_sha256"], bundle_sha256)

    def test_graph_sources_and_payload_citations_share_the_same_instance(self):
        source_ids = {source["id"] for source in self.package["sources"]}
        self.assertEqual(source_ids, set(self.manifest["material_source_ids"]))
        self.assertEqual(set(self.binding["page_sources"]["page1"])
                         | set(self.binding["page_sources"]["page2"])
                         | set(self.binding["page_sources"]["page3"]), source_ids)
        for node in self.graph["nodes"]:
            referenced_file = node["path"].split("#", 1)[0]
            self.assertTrue((BASE / referenced_file).exists(), node["path"])
            self.assertTrue(set(node["depends_on"]).issubset({n["id"] for n in self.graph["nodes"]}))

    def test_square_payload_reaches_executive_renderer(self):
        html, checks = R(self.payload).build()
        self.assertEqual(html.count('<section class="page">'), 3)
        self.assertIn("SQUARE MANAGEMENT", html)
        self.assertIn("G-C1", checks)

    def test_ci_discovers_bound_independent_company_runs(self):
        self.assertIn("square-management", {run[0] for run in bound_runs(ROOT)})

    def test_ci_rejects_payload_changed_without_rerendering(self):
        with tempfile.TemporaryDirectory() as tmp:
            temp_root = Path(tmp)
            shutil.copytree(BASE, temp_root / "companies" / "square-management")
            payload_path = temp_root / "companies/square-management/outputs/square-management-exec-payload.json"
            payload = read_json(payload_path)
            payload["page1"]["thesis"]["paras"][0] += " Modified after evidence review."
            payload_path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
            with self.assertRaisesRegex(ValueError, "stale payload hash"):
                bound_runs(temp_root)

    def test_pdf_and_reviews_are_bound_to_payload_and_manifest(self):
        pdf = BASE / "outputs/Square_Management_3pager.pdf"
        self.assertEqual(len(PdfReader(str(pdf)).pages), 3)
        self.assertEqual(self.binding["payload"], self.manifest["payload_ref"])
        self.assertEqual(self.binding["graph"], self.manifest["graph_ref"])
        self.assertEqual(self.manifest["pdf_ref"], "companies/square-management/outputs/Square_Management_3pager.pdf")
        self.assertEqual(self.render_manifest["payload_sha256"], sha256(self.payload_path))
        self.assertEqual(self.render_manifest["pdf_sha256"], sha256(pdf))
        self.assertEqual(self.render_manifest["page_count"], 3)
        self.assertEqual(len(self.manifest["review_refs"]), 3)
        for ref in self.manifest["review_refs"]:
            self.assertTrue((ROOT / ref).exists(), ref)


if __name__ == "__main__":
    unittest.main()
