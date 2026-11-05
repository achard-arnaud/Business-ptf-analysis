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
            for numbers in ([1,2,3,4,5],[1,2,3,4,5,5]):
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
        self.assertIn('<b>1</b> Coût',output)
        self.assertNotIn('<table',output)

    @unittest.skipUnless(os.environ.get('PEDAGOGICAL_BROWSER_TEST')=='1','browser test enabled by render workflow')
    def test_browser_rejects_overflow(self):
        with tempfile.TemporaryDirectory() as folder:
            folder=Path(folder);source=folder/'overflow.md'
            source.write_text('# Test\n'+''.join(f'## Page {n} — Test\n'+('Débordement volontaire. '*2200 if n==1 else 'Contenu suffisant pour vérifier la page physique. '*4)+'\n' for n in range(1,7)))
            binding=r.bind(source);html=folder/'fiche.html';html.write_text(r.compose(binding))
            report,_=asyncio.run(r.render_artifacts(html,folder))
            self.assertFalse(report['pass'])
            self.assertGreater(report['summary']['overflows']+report['summary']['out_of_bounds'],0)

if __name__=='__main__':unittest.main()
