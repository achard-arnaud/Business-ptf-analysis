import asyncio,copy,importlib.util,json,os,sys,tempfile,unittest
from io import BytesIO
from pathlib import Path
from unittest.mock import patch
from pypdf import PdfReader, PdfWriter
from pypdf.annotations import Link
from pypdf.generic import ArrayObject, ContentStream, DecodedStreamObject, DictionaryObject, NameObject, TextStringObject
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'renderers/pedagogical'))
import landscape as renderer
SOURCE=ROOT/'learning/enterprise-ai/perception.sheet.json'


def tagged_fixture_links(pdf_bytes, page_index=0):
    """Read explicit link ownership on the selected page of a Chromium fixture."""
    pdf = PdfReader(BytesIO(pdf_bytes))
    if '/StructTreeRoot' not in pdf.root_object:
        raise ValueError('expected a tagged PDF')
    annotations = {
        ref: str(ref.get_object()['/A']['/URI'])
        for ref in pdf.pages[page_index].get('/Annots', [])
        if ref.get_object().get('/Subtype') == '/Link'
        and ref.get_object().get('/A', {}).get('/S') == '/URI'
    }

    def nodes(value):
        obj = value.get_object()
        if isinstance(obj, ArrayObject):
            for child in obj:
                yield from nodes(child)
        else:
            yield obj
            if isinstance(obj, DictionaryObject) and '/K' in obj:
                yield from nodes(obj['/K'])

    def marked_text(mcids):
        writer = PdfWriter(clone_from=BytesIO(pdf_bytes))
        page = writer.pages[page_index]
        # Keep font-encoded bytes intact while filtering text-show operators.
        content = ContentStream(page.get_contents(), writer, 'bytes')
        stack = []
        selected = []
        for operands, operator in content.operations:
            if operator in (b'BDC', b'BMC'):
                props = operands[1].get_object() if operator == b'BDC' else None
                stack.append(props.get('/MCID') if isinstance(props, DictionaryObject) else None)
            elif operator == b'EMC':
                stack.pop()
            if operator not in (b'Tj', b'TJ', b"'", b'"') or any(key in mcids for key in stack):
                selected.append((operands, operator))
        content.operations = selected
        page.replace_contents(content)
        return ' '.join(page.extract_text().split())

    links = {}
    seen_refs, seen_mcids = set(), set()
    for node in nodes(pdf.root_object['/StructTreeRoot']['/K']):
        if not isinstance(node, DictionaryObject) or node.get('/S') != '/Link':
            continue
        kids = list(nodes(node['/K']))
        refs = [kid.raw_get('/Obj') for kid in kids
                if isinstance(kid, DictionaryObject) and kid.get('/Type') == '/OBJR']
        # MCIDs can repeat across physical pages. Select the link by the actual
        # annotation refs on this page before reading its marked text.
        if len(pdf.pages) > 1 and not annotations.keys() & set(refs):
            continue
        mcids = {int(kid) for kid in kids if isinstance(kid, int)}
        mcids.update(int(kid['/MCID']) for kid in kids
                     if isinstance(kid, DictionaryObject) and kid.get('/Type') == '/MCR')
        if (not refs or not mcids or len(set(refs)) != len(refs) or seen_refs.intersection(refs)
                or seen_mcids.intersection(mcids) or not set(refs).issubset(annotations)):
            raise ValueError('missing or ambiguous link ownership')
        text = marked_text(mcids)
        if not text or text in links:
            raise ValueError('missing or ambiguous marked link text')
        links[text] = {annotations[ref] for ref in refs}
        seen_refs.update(refs)
        seen_mcids.update(mcids)
    if not annotations or seen_refs != annotations.keys():
        raise ValueError('missing or ambiguous link ownership')
    return links


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

    def _verify_citation_fixture(self, missing_from):
        with tempfile.TemporaryDirectory() as folder:
            root = Path(folder)
            url = 'https://example.org/source'
            sheet = {
                'catalog_ref': 'catalog.json',
                'title': 'Synthetic fixture', 'subtitle': 'Six pages',
                'sources': [{'id': 'S1', 'url': url, 'title': 'Synthetic source',
                             'locator': 'Section 1', 'status': 'source'},
                            {'id': 'S2', 'url': '', 'title': 'Provided corpus',
                             'locator': 'Section 2', 'status': 'source'},
                            {'id': 'S3', 'url': url, 'title': 'Same report — second section',
                             'locator': 'Section 3', 'status': 'source'}],
                'pages': [{'title': f'Section {index+1}', 'lead': 'Synthetic lead',
                           'content': {}, 'kind': 'understand', 'takeaway': 'Synthetic takeaway',
                           'source_ids': ['S1', 'S2', 'S3'] if index in (0, 2) else []}
                          for index in range(6)],
            }
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
            expected_markdown = renderer.as_markdown(sheet)
            (out / 'fiche.md').write_text(expected_markdown)
            for n in range(1, 7):
                (out / f'page-{n:02d}.png').write_bytes(b'screenshot placeholder')
            def write_pdf(link_pages, label_pages=(0, 2), second_citation_pages=(0, 2)):
                pdf = PdfWriter()
                for _ in range(6):
                    pdf.add_blank_page(width=842, height=595)
                for index in link_pages:
                    pdf.add_annotation(page_number=index, annotation=Link(rect=(10, 10, 80, 30), url=url))
                for index in set(label_pages) | set(link_pages):
                    page = pdf.pages[index]
                    names = NameObject
                    page[names('/Resources')] = DictionaryObject({names('/Font'): DictionaryObject({
                        names('/F1'): DictionaryObject({names('/Type'): names('/Font'),
                            names('/Subtype'): names('/Type1'), names('/BaseFont'): names('/Helvetica')})})})
                    stream = DecodedStreamObject()
                    text_rows = []
                    if index in link_pages:
                        text_rows.append(b'S1 Synthetic source')
                        if index in second_citation_pages:
                            text_rows.extend([b'S3 Same', b'report'])
                            pdf.add_annotation(page_number=index, annotation=Link(rect=(90, 10, 180, 30), url=url))
                    if index in label_pages:
                        text_rows.extend([b'S2 Corpus', b'fourni'])
                    stream.set_data(b'BT /F1 12 Tf 30 135 Td (' + b') Tj 0 -14 Td ('.join(text_rows) + b') Tj ET')
                    page.replace_contents(stream)
                pdf.write(out / 'fiche.pdf')

            def write_receipt():
                outputs = {p.name: renderer.sha(p) for p in out.iterdir() if p.name != 'qa.json'}
                qa = {'pass': True, 'source_sha256': renderer.sha(source),
                      'catalog_sha256': renderer.sha(catalog), 'outputs': outputs,
                      'runtime_hashes': {}, 'summary': {}}
                (out / 'qa.json').write_text(json.dumps(qa))

            # Isolate projection checks using actual six-page PDF annotations.
            with patch.object(renderer, 'load_sheet', return_value=sheet), \
                 patch.object(renderer, 'scaffold', return_value=scaffold):
                write_pdf((0, 2))
                (out / 'fiche.html').write_text(expected_html)
                write_receipt()
                self.assertTrue(renderer.verify(source, out)['pass'])
                if missing_from == 'html':
                    (out / 'fiche.html').write_text(expected_html.replace(citation, ''))
                    message = 'HTML does not match scaffold and theme'
                elif missing_from == 'pdf':
                    write_pdf((2,))  # Same destination on page 3 cannot satisfy page 1.
                    message = 'PDF page 1 is missing source link S1'
                elif missing_from == 'markdown':
                    citation_line = next(line for line in expected_markdown.splitlines(keepends=True)
                                         if line.startswith('- **S1** '))
                    (out / 'fiche.md').write_text(expected_markdown.replace(citation_line, '', 1))
                    message = 'Markdown does not match canonical sheet'
                elif missing_from == 'pdf-linked-label':
                    write_pdf((0, 2), second_citation_pages=(2,))
                    message = 'PDF page 1 is missing source label S3'
                else:
                    write_pdf((0, 2), label_pages=(2,))
                    message = 'PDF page 1 is missing source label S2'
                write_receipt()
                with self.assertRaisesRegex(ValueError, message):
                    renderer.verify(source, out)

    def test_verify_rejects_missing_html_citation_even_with_matching_hash(self):
        self._verify_citation_fixture('html')

    def test_verify_rejects_pdf_link_missing_from_required_page_even_with_matching_hash(self):
        self._verify_citation_fixture('pdf')

    def test_verify_rejects_missing_markdown_source_even_with_matching_hash(self):
        self._verify_citation_fixture('markdown')

    def test_verify_rejects_missing_unlinked_pdf_source_even_with_matching_hash(self):
        self._verify_citation_fixture('pdf-text')

    def test_verify_rejects_missing_pdf_citation_when_its_url_is_used_by_another(self):
        self._verify_citation_fixture('pdf-linked-label')

    @unittest.skipUnless(os.environ.get('PEDAGOGICAL_BROWSER_TEST')=='1','real browser enabled by CI')
    def test_chromium_pdf_links_preserve_destination_per_text_line(self):
        from playwright.async_api import async_playwright

        first = 'https://example.invalid/first'
        second = 'https://example.invalid/second'
        canonical = [(first,), (first,), (second,)]

        async def check():
            async with async_playwright() as playwright:
                browser = await renderer.legacy.launch(playwright)
                try:
                    page = await browser.new_page(viewport={'width': 480, 'height': 320})
                    await page.emulate_media(media='print')
                    for swapped in (False, True):
                        with self.subTest(swapped=swapped):
                            s1, s2 = (second, first) if swapped else (first, second)
                            await page.set_content(f'''<!DOCTYPE html><style>
                                @page {{ size: 480px 320px; margin: 0; }}
                                body {{ margin: 0; font: 20px/32px sans-serif; }}
                                #s1, #s2 {{ position: absolute; }}
                                #s1 {{ left: 36px; top: 30px; }}
                                #s2 {{ left: 180px; top: 190px; }}
                            </style>
                            <div id="s1"><a href="{s1}"><span>S1 Long source</span><br>
                                <span>second line</span></a></div>
                            <div id="s2"><a href="{s2}"><span>S2 Short source</span></a></div>''')
                            lines = await page.locator('a').evaluate_all('''anchors => anchors.map(a =>
                                Array.from(a.querySelectorAll('span'), span =>
                                    Array.from(span.getClientRects(), r =>
                                        [r.x + r.width / 2, r.y + r.height / 2])))''')
                            self.assertEqual([[len(rects) for rects in anchor] for anchor in lines],
                                             [[1, 1], [1]])
                            self.assertLess(lines[0][0][0][1], lines[0][1][0][1])
                            pdf = PdfReader(BytesIO(await page.pdf(prefer_css_page_size=True, scale=1)))
                            self.assertEqual(len(pdf.pages), 1)
                            printed = pdf.pages[0]
                            media = printed.mediabox
                            sx, sy = float(media.width) / 480, float(media.height) / 320
                            links = []
                            for ref in printed.get('/Annots', []):
                                annotation = ref.get_object()
                                action = annotation.get('/A', {})
                                if annotation.get('/Subtype') == '/Link' and action.get('/S') == '/URI':
                                    links.append((tuple(map(float, annotation['/Rect'])), str(action['/URI'])))

                            # DOM positions run down from the top; PDF points run up from the bottom.
                            found = []
                            for anchor in lines:
                                for [(css_x, css_y)] in anchor:
                                    x = float(media.left) + sx * css_x
                                    y = float(media.top) - sy * css_y
                                    found.append(tuple(uri for (left, bottom, right, top), uri in links
                                                       if left < x < right and bottom < y < top))
                            self.assertEqual(found, [(second,), (second,), (first,)] if swapped else canonical)
                finally:
                    await browser.close()

        asyncio.run(check())

    @unittest.skipUnless(os.environ.get('PEDAGOGICAL_BROWSER_TEST')=='1','real browser enabled by CI')
    def test_chromium_tagged_pdf_links_identify_text_without_html_coordinates(self):
        from playwright.async_api import async_playwright

        first, second = ('https://example.invalid/first', 'https://example.invalid/second')
        multiline, other = 'Alpha reference continued', 'Beta reference'

        async def render_sample():
            async with async_playwright() as playwright:
                browser = await renderer.legacy.launch(playwright)
                try:
                    page = await browser.new_page()
                    await page.set_content(f'''<!DOCTYPE html><html lang="en"><title>Links fixture</title>
                        <style>body {{ font: 20px/32px sans-serif; }}</style>
                        <p><a href="{first}">Alpha reference<br>continued</a></p>
                        <p><a href="{second}">Beta reference</a></p></html>''')
                    return await page.pdf(tagged=True)
                finally:
                    await browser.close()

        original = asyncio.run(render_sample())
        self.assertEqual(tagged_fixture_links(original), {multiline: {first}, other: {second}})

        def rewrite(swap_destinations=False, remove_reference=False):
            writer = PdfWriter(clone_from=BytesIO(original))
            page = writer.pages[0]
            refs = list(reversed(page['/Annots']))
            if swap_destinations:
                for ref in refs:
                    action = ref.get_object()['/A']
                    action[NameObject('/URI')] = TextStringObject({first: second, second: first}[action['/URI']])
            page[NameObject('/Annots')] = ArrayObject(refs[1:] if remove_reference else refs)
            buffer = BytesIO()
            writer.write(buffer)
            return buffer.getvalue()

        self.assertEqual(tagged_fixture_links(rewrite()), {multiline: {first}, other: {second}})
        self.assertEqual(tagged_fixture_links(rewrite(swap_destinations=True)),
                         {multiline: {second}, other: {first}})
        with self.assertRaisesRegex(ValueError, 'missing or ambiguous link ownership'):
            tagged_fixture_links(rewrite(remove_reference=True))

    @unittest.skipUnless(os.environ.get('PEDAGOGICAL_BROWSER_TEST')=='1','real browser enabled by CI')
    def test_perception_tagged_pdf_preserves_page_scoped_source_links(self):
        from playwright.async_api import async_playwright

        sheet = renderer.load_sheet(SOURCE)
        sources = {source['id']: source for source in sheet['sources']}
        expected = [{renderer.linked_source_label(sources[k]): {sources[k]['url']}
                     for k in spec['source_ids'] if sources[k]['url']}
                    for spec in sheet['pages']]
        self.assertEqual([len(links) for links in expected], [5, 2, 1, 1, 1, 1])

        async def render_pair():
            async with async_playwright() as playwright:
                browser = await renderer.legacy.launch(playwright)
                try:
                    page = await browser.new_page(viewport={'width': 1250, 'height': 900}, device_scale_factor=1.5)
                    await page.route('**/*', lambda route: route.abort())
                    await page.set_content(renderer.styled_document(renderer.scaffold(sheet)))
                    await page.evaluate('document.fonts.ready')
                    opts = dict(format='A4', landscape=True, print_background=True, prefer_css_page_size=True)
                    return await page.pdf(tagged=False, **opts), await page.pdf(tagged=True, **opts)
                finally:
                    await browser.close()

        plain, tagged = asyncio.run(render_pair())
        ordinary, structured = (PdfReader(BytesIO(raw)) for raw in (plain, tagged))
        self.assertEqual(len(ordinary.pages), 6)
        self.assertEqual(len(structured.pages), 6)
        for index, (before, after) in enumerate(zip(ordinary.pages, structured.pages)):
            with self.subTest(page=index+1):
                self.assertEqual(tuple(before.mediabox), tuple(after.mediabox))
                self.assertEqual(before.extract_text(), after.extract_text())
                self.assertEqual(tagged_fixture_links(tagged, index), expected[index])
        renderer.verify_pdf_sources(structured, sheet)

        # Keep the PDF text and annotations on pages 2–6 intact. Only exchange
        # the URI of two existing annotations on page 1, even though S1 repeats.
        writer = PdfWriter(clone_from=BytesIO(tagged))
        labels = [renderer.linked_source_label(sources[k]) for k in ('S1', 'S3')]
        first, second = (sources[k]['url'] for k in ('S1', 'S3'))
        count = 0
        for ref in writer.pages[0]['/Annots']:
            action = ref.get_object()['/A']
            url = action.get('/URI')
            if url in (first, second):
                action[NameObject('/URI')] = TextStringObject(second if url == first else first)
                count += 1
        self.assertEqual(count, 2)
        crossed = BytesIO()
        writer.write(crossed)
        mutated = crossed.getvalue()
        self.assertEqual(PdfReader(BytesIO(mutated)).pages[0].extract_text(), structured.pages[0].extract_text())
        for index, original in enumerate(expected):
            got = tagged_fixture_links(mutated, index)
            self.assertEqual(set(got), set(original))
            with self.subTest(crossed=True, page=index+1):
                self.assertEqual({label for label in original if original[label] != got[label]},
                                 set(labels) if index == 0 else set())

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
