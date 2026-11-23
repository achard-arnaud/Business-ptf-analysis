"""Regression tests for the independent executive presentation contract."""
import copy
import json
import sys
import unittest
from unittest.mock import patch
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / 'renderers' / 'three_pager_exec'))
from render_exec import CoherenceError, R  # noqa: E402
sys.path.insert(0, str(ROOT / 'scripts'))
from validate_exec import validate_exec_payload  # noqa: E402
from validate import digest  # noqa: E402

BASE = json.loads((ROOT / 'tests/fixtures/exec/sphere_unverified_v0.3.json').read_text(encoding='utf-8'))


class ExecContract(unittest.TestCase):
    def mutate(self, change):
        data = copy.deepcopy(BASE)
        change(data)
        with self.assertRaises(CoherenceError):
            R(data).build()

    def test_reference_compiles_as_demo(self):
        html, checks = R(BASE).build()
        self.assertEqual(html.count('<section class="page">'), 3)
        self.assertIn('G-C1', checks)

    def test_required_footer_body_must_contain_text(self):
        for page in ('page1', 'page2', 'page3'):
            for body in (None, '', ' \t '):
                with self.subTest(page=page, body=body):
                    data = copy.deepcopy(BASE)
                    footer = data[page]['footer']
                    if body is None:
                        del footer['body']
                        field = f"{page}/footer: 'body'"
                    else:
                        footer['body'] = body
                        field = f'{page}/footer/body:'
                    with self.assertRaisesRegex(CoherenceError, f'^SCHEMA: {field}'):
                        R(data).build()

    def test_nonblank_conclusion_still_requires_posture(self):
        data = copy.deepcopy(BASE)
        data['page3']['footer']['body'] = 'Une conclusion sans la posture attendue.'
        with self.assertRaisesRegex(CoherenceError, '^G-C4: .*conclusion'):
            R(data).build()

    def test_thesis_requires_two_nonblank_text_paragraphs(self):
        for index in (0, 1):
            for body in ("", " \t ", None, 17):
                with self.subTest(index=index, body=body):
                    data = copy.deepcopy(BASE)
                    data["page1"]["thesis"]["paras"][index] = body
                    with self.assertRaisesRegex(CoherenceError, f"^SCHEMA: page1/thesis/paras/{index}:"):
                        R(data).build()

    def test_orphan_reference(self):
        self.mutate(lambda p: p['page2']['primary'][1].pop('themes'))

    def test_three_stars_require_reference(self):
        self.mutate(lambda p: p['page2']['support'][0].update(themes=[]))

    def test_driver_coverage(self):
        self.mutate(lambda p: p['transformation'].update(covers=[]))

    def test_duplicate_driver(self):
        self.mutate(lambda p: p['drivers'][1].update(id=p['drivers'][0]['id']))

    def test_quadrant_coverage(self):
        self.mutate(lambda p: p['page3']['quadrant']['cells'].pop(4))

    def test_posture_alignment(self):
        self.mutate(lambda p: p['posture'].update(current='S-O', label='offensive'))

    def test_figure_reference(self):
        self.mutate(lambda p: p['page1']['signaletique']['rows'].append(['X', '{absent}']))

    def test_forbidden_disclaimer(self):
        self.mutate(lambda p: p['page2']['lecture'].update(text='Ce n’est pas un business case.'))

    def test_internal_id(self):
        self.mutate(lambda p: p['themes'][0].update(change='Voir UC-S09'))

    def test_missing_takeaway(self):
        self.mutate(lambda p: p['page1']['thesis'].update(take=''))

    def test_too_many_themes(self):
        self.mutate(lambda p: p['themes'].extend([dict(p['themes'][0], n=k) for k in (5, 6)]))

    def test_strategy_family_without_theme(self):
        self.mutate(lambda p: p['page3']['dominant']['rows'].append(['Résilience', 'resilience']))

    def test_top_count(self):
        self.mutate(lambda p: p['page2'].update(top_count=3))

    def test_porter_shape(self):
        self.mutate(lambda p: p['page2']['primary'].pop())

    def test_porter_names(self):
        self.mutate(lambda p: p['page2']['primary'][0].update(name='Autre activité'))

    def test_cutoff_date_format(self):
        self.mutate(lambda p: p.update(cutoff='tomorrow'))

    def test_layout_cannot_inject_markup(self):
        self.mutate(lambda p: p.update(layout={'p1_rows': '1fr; color:red'}))

    def test_fixture_not_bound_to_current_bundle(self):
        with patch('validate_exec.validate_bundle', return_value={'snapshot_integrity': 'verified'}):
            with self.assertRaisesRegex(ValueError, 'cutoff'):
                validate_exec_payload(BASE, ROOT / 'companies/sphere', '/tmp/archive.json')

    def test_bundle_binding_requires_hash_and_registered_figure_sources(self):
        base = ROOT / 'companies/sphere'
        p = copy.deepcopy(BASE)
        p['cutoff'] = '2026-09-23'
        with patch('validate_exec.validate_bundle', return_value={'snapshot_integrity': 'verified'}):
            with self.assertRaisesRegex(ValueError, 'hash'):
                validate_exec_payload(p, base, '/tmp/archive.json')
            package = json.loads((base / 'package.json').read_text())
            context = json.loads((base / 'strategic_context.json').read_text())
            graph = json.loads((base / 'research_graph.json').read_text())
            p['lineage']['bundle_sha256'] = digest({'package': package, 'context': context, 'graph': graph})
            p['figures']['ca25']['src'] = 'unknown'
            with self.assertRaisesRegex(ValueError, 'unknown source'):
                validate_exec_payload(p, base, '/tmp/archive.json')


if __name__ == '__main__':
    unittest.main()
