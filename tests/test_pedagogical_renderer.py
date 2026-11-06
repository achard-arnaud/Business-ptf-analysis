import asyncio
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('pedagogical_render',ROOT/'renderers/pedagogical/render.py')
r=importlib.util.module_from_spec(spec);spec.loader.exec_module(r)

class PedagogicalRendererTests(unittest.TestCase):
    def test_reject_missing_or_duplicate_pages(self):
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'input.md'
            for numbers in ([1,2,3,4,5],[1,2,3,4,5,5],[1,2,3,4,5,6,7]):
                source.write_text('\n'.join(f'## Page {n} — Test\nContenu' for n in numbers))
                with self.assertRaises(ValueError):r.bind(source)

    def test_upstream_imports_are_unchanged(self):
        lock=json.loads((r.HERE/'upstream-lock.json').read_text())
        for item in lock['imports']:
            self.assertEqual(r.digest(r.HERE/item['local_path']),item['sha256'])

    def test_bac_projection_preserves_text_and_scores(self):
        table=['| Cas | BAC | Valeur | Coût | Risque | Complexité | Généricité |',
               '|---|---|---|---|---|---|---|',
               '| Un cas unique | B : texte source; A : avantage; C : champ | 3 | 1 | 2 | 2 | 3 |']
        output=r.table_component(table,6)
        self.assertIn('Un cas unique',output)
        self.assertIn('texte source',output)
        self.assertIn('data-score="1"',output)
        self.assertIn('★',output)
        self.assertNotIn('<table',output)

    def test_existing_modules_and_css_free_scaffold(self):
        for source in (ROOT/'learning/enterprise-ai').glob('*.md'):
            if source.stem not in ('prediction','perception','creation','reasoning','agentic','multicapability'): continue
            binding=r.bind(source)
            self.assertEqual([p['page_id'] for p in binding['pages']],['p1','p2','p3','p4','p5','p6'])
            self.assertNotIn('<style',r.compose(binding,include_styles=False))
            self.assertIn('<style',r.compose(binding))

    def test_reject_invalid_score_empty_page_and_case_count(self):
        text=(ROOT/'tests/fixtures/perception-v2.md').read_text()
        invalid_score=text.replace('| 3 | 2 | 2 | 2 | 3 |','| 4 | 2 | 2 | 2 | 3 |')
        invalid_page=text[:text.index('## Page 3')]+text[text.index('## Page 4'):]
        case_rows=[line for line in text.splitlines() if line.startswith('| Extraction') or line.startswith('| Transcription')]
        invalid_cases=text
        for line in case_rows: invalid_cases=invalid_cases.replace(line,'')
        with tempfile.TemporaryDirectory() as folder:
            source=Path(folder)/'invalid.md'
            for content in (invalid_score,invalid_page,invalid_cases):
                source.write_text(content)
                with self.assertRaises(ValueError): r.bind(source)
            binding=r.bind(ROOT/'tests/fixtures/perception-v2.md')
            binding['pages'][2]['markdown']=' '
            with self.assertRaises(ValueError):r.validate_binding(binding)

    def test_verifier_rejects_source_and_output_tampering(self):
        v=r.module('pedagogical_verify',r.HERE/'verify.py')
        with tempfile.TemporaryDirectory() as folder:
            out=Path(folder);source=out/'source.md';source.write_text('original')
            for name in v.REQUIRED:(out/name).write_text('artifact')
            manifest={'source_sha256':r.digest(source),'outputs':[{'path':name,'sha256':r.digest(out/name)} for name in v.REQUIRED]}
            v.verify_hashes(source,out,manifest)
            source.write_text('modified')
            with self.assertRaises(ValueError):v.verify_hashes(source,out,manifest)
            source.write_text('original');(out/'binding.json').write_text('modified')
            with self.assertRaises(ValueError):v.verify_hashes(source,out,manifest)

    @unittest.skipUnless(os.environ.get('PEDAGOGICAL_BROWSER_TEST')=='1','browser test enabled by render workflow')
    def test_browser_rejects_overflow(self):
        with tempfile.TemporaryDirectory() as folder:
            folder=Path(folder);source=folder/'overflow.md'
            text=(ROOT/'tests/fixtures/perception-v2.md').read_text()
            source.write_text(text.replace('## Page 2', ('Débordement volontaire. '*2200)+'\n\n## Page 2'))
            binding=r.bind(source);html=folder/'fiche.html';html.write_text(r.compose(binding))
            report,_=asyncio.run(r.render_artifacts(html,folder))
            self.assertFalse(report['pass'])
            self.assertGreater(report['summary']['overflows']+report['summary']['out_of_bounds'],0)

if __name__=='__main__':unittest.main()
