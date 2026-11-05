"""Tests for the explicit one-skill discovery and document route."""
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from check_skill_docs import check, check_document, check_frontmatter  # noqa: E402


class SkillDocs(unittest.TestCase):
    def test_real_route_documents_exist(self):
        self.assertEqual(check(ROOT), [])

    def test_broken_local_link_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "doc.md"
            page.write_text("[bad](missing.md)", encoding="utf-8")
            self.assertTrue(check_document(page, root))
            (root / "missing.md").write_text("ok", encoding="utf-8")
            self.assertEqual(check_document(page, root), [])

    def test_local_link_escape_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            page = root / "doc.md"
            page.write_text("[unsafe](../../outside.md)", encoding="utf-8")
            self.assertTrue(check_document(page, root))

    def test_bad_frontmatter_fails(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp) / "some-skill"
            root.mkdir()
            path = root / "SKILL.md"
            path.write_text("# no metadata", encoding="utf-8")
            self.assertTrue(check_frontmatter(path))
            path.write_text("---\nname: wrong\ndescription: foo\n---\n", encoding="utf-8")
            self.assertTrue(check_frontmatter(path))
            path.write_text("---\nname: some-skill\ndescription: foo\n---\n", encoding="utf-8")
            self.assertEqual(check_frontmatter(path), [])


if __name__ == "__main__":
    unittest.main()
