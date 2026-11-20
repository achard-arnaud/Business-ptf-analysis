import asyncio,copy,importlib.util,json,os,sys,tempfile,unittest
from pathlib import Path
from unittest.mock import patch
from pypdf import PdfWriter
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderers/pedagogical'))
import landscape as renderer
SOURCE=ROOT/'learning/enterprise-ai/perception.sheet.json'

class LandscapeTests(unittest.TestCase):
    def test_content_separation_and_source_links(self):
        sheet=renderer.load_sheet(SOURCE);scaffold=renderer.scaffold(sheet)
        self.assertNotIn('<style',scaffold)
        self.assertEqual(scaffold.count('<section class="page '),6)
        self.assertIn('Cinq causes systémiques',scaffold)
        self.assertIn('932 millions',scaffold)
        self.assertIn('https://www.bmwgroup.com/',scaffold)
        self.assertEqual([x['id'] for x in sheet['pages'][5]['content']['use_cases']],['UC-021','UC-042','UC-041','UC-044'])

    def test_unknown_sources_and_invented_cases_fail(self):
        for kind in ('source','case','score','presentation'):
            sheet=json.loads(SOURCE.read_text())
            if kind=='source':sheet['pages'][0]['source_ids'].append('S999')
            if kind=='case':sheet['pages'][5]['content']['use_cases'][0]['id']='UC-999'
            if kind=='score':sheet['pages'][5]['content']['use_cases'][0]['scores'][0]=0
            if kind=='presentation':sheet['pages'][0]['content']['definition']='<div>hidden layout</div>'
            with self.assertRaises(ValueError):renderer.validate(sheet,SOURCE.parent)

    def test_do_not_collapse_autopilot_and_agent(self):
        sheet=renderer.load_sheet(SOURCE);levels=sheet['pages'][3]['content']['levels']
        self.assertEqual([(x['integration'],x['automation']) for x in levels],[('Faible','Faible'),('Forte','Faible'),('Faible','Forte'),('Forte','Forte')])
        levels[2]['name']='Agent'
        with self.assertRaises(ValueError):renderer.validate(sheet,SOURCE.parent)

    def test_catalog_preserves_70_distinct_situations_and_classical_options(self):
        c=json.loads((SOURCE.parent/'use-cases.catalog.json').read_text());items={x['id']:x for x in c['items']}
        self.assertEqual(set(items),{f'UC-{n:03d}' for n in range(1,71)})
        self.assertIsNone(items['UC-035']['primary_capability']);self.assertIsNone(items['UC-068']['primary_capability'])
        self.assertEqual(items['UC-042']['primary_capability'],'perception')
        self.assertIn('sans intervention humaine',items['UC-021']['situation_originale'])
        self.assertIn('règle fixe',items['UC-046']['explanation_originale'])

    def test_markdown_is_regenerated_from_canonical_sheet(self):
        sheet=renderer.load_sheet(SOURCE)
        self.assertEqual(renderer.as_markdown(sheet),(SOURCE.parent/'perception.md').read_text())
        self.assertEqual(renderer.as_markdown(sheet).count('## Page '),6)

    def test_verify_rejects_missing_html_citation_even_with_matching_hash(self):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            sheet = {'catalog_ref': 'catalog.json'}
            source = root / 'sheet.json'
            source.write_text(json.dumps(sheet))
            catalog = root / 'catalog.json'
            catalog.write_text('{}')
            out = root / 'out'
            out.mkdir()
            citation = '<a href="https://example.org/source">S1 Synthetic source</a>'
            scaffold = f'<html><head></head><body>{citation}</body></html>'
            theme = (renderer.HERE / 'landscape.css').read_text()
            expected_html = scaffold.replace('</head>', f'<style>{theme}</style></head>')
            (out / 'binding.json').write_text(json.dumps(sheet))
            (out / 'scaffold.html').write_text(scaffold)
            (out / 'fiche.md').write_text('Synthetic content')
            for n in range(1, 7):
                (out / f'page-{n:02d}.png').write_bytes(b'screenshot placeholder')
            pdf = PdfWriter()
            for _ in range(6):
                pdf.add_blank_page(width=842, height=595)
            pdf.write(out / 'fiche.pdf')

            def write_html_and_receipt(html):
                (out / 'fiche.html').write_text(html)
                outputs = {p.name: renderer.sha(p) for p in out.iterdir() if p.name != 'qa.json'}
                qa = {'pass': True, 'source_sha256': renderer.sha(source),
                      'catalog_sha256': renderer.sha(catalog), 'outputs': outputs,
                      'runtime_hashes': {}, 'summary': {}}
                (out / 'qa.json').write_text(json.dumps(qa))

            # Isolate the projection check from story generation and browser QA.
            with patch.object(renderer, 'load_sheet', return_value=sheet), \
                 patch.object(renderer, 'scaffold', return_value=scaffold):
                write_html_and_receipt(expected_html)
                self.assertTrue(renderer.verify(source, out)['pass'])
                write_html_and_receipt(expected_html.replace(citation, ''))
                with self.assertRaisesRegex(ValueError, 'HTML does not match scaffold and theme'):
                    renderer.verify(source, out)

    @unittest.skipUnless(os.environ.get('PEDAGOGICAL_BROWSER_TEST')=='1','real browser enabled by CI')
    def test_landscape_overflow_is_rejected(self):
        sheet=renderer.load_sheet(SOURCE)
        sheet['pages'][0]['content']['definition']='Débordement volontaire. '*3000
        with tempfile.TemporaryDirectory() as folder:
            root=Path(folder);source=root/'perception.sheet.json';source.write_text(json.dumps(sheet,ensure_ascii=False))
            (root/sheet['catalog_ref']).write_text((SOURCE.parent/sheet['catalog_ref']).read_text())
            report=asyncio.run(renderer.render(source,root/'out'))
            self.assertFalse(report['pass'])
            with self.assertRaises(ValueError):renderer.verify(source,root/'out')

if __name__=='__main__':unittest.main()
