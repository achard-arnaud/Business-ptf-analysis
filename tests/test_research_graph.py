"""Tests for bounded traversal of a synthetic dependency graph."""
import importlib.util
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
SPEC = importlib.util.spec_from_file_location('research_graph', ROOT / 'scripts/research_graph.py')
graph = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(graph)


class CountingDependencies(list):
    traversals = 0

    def __iter__(self):
        self.traversals += 1
        return super().__iter__()


class ResearchGraphTests(unittest.TestCase):
    def setUp(self):
        self.shared = CountingDependencies(['source'])
        self.data = {'nodes': [
            {'id': 'source', 'depends_on': []},
            {'id': 'common', 'depends_on': self.shared},
            {'id': 'left', 'depends_on': ['common']},
            {'id': 'right', 'depends_on': ['common']},
            {'id': 'output', 'depends_on': ['right', 'left']},
            {'id': 'independent', 'depends_on': []},
        ]}

    def test_shared_ancestry_has_one_visit_per_pass(self):
        result = graph.context(self.data, 'output', budget=5)
        self.assertEqual([n['id'] for n in result], ['source', 'common', 'right', 'left', 'output'])
        self.assertLessEqual(self.shared.traversals, 2)  # Validation and context selection.

    def test_budget_and_affected_scope_keep_their_boundaries(self):
        with self.assertRaisesRegex(ValueError, 'context budget exceeded'):
            graph.context(self.data, 'output', budget=4)
        self.assertEqual(graph.affected(self.data, 'left'), ['left', 'output'])
        self.assertEqual(graph.affected(self.data, 'common'), ['common', 'left', 'output', 'right'])

    def test_disconnected_invalid_dependencies_are_still_rejected(self):
        for dependency, error in [('missing', 'dangling graph dependency'),
                                  ('independent', 'graph cycle')]:
            with self.subTest(dependency=dependency):
                self.data['nodes'][-1]['depends_on'] = [dependency]
                with self.assertRaisesRegex(ValueError, error):
                    graph.context(self.data, 'output')
