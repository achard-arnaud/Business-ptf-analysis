import importlib.util
import unittest
import shutil
from pathlib import Path
import test_case_runtime as case_tests
engine = case_tests.engine

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('technical_io', ROOT / 'scripts/technical_decision.py')
technical = importlib.util.module_from_spec(spec)
spec.loader.exec_module(technical)


class TechnicalDecisionTests(unittest.TestCase):
    def setUp(self):
        case_tests.CaseRuntimeTests.setUp(self)
        for path in ('config/technical-decisions.json', 'contracts/technical-decision.schema.json'):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)

    def memo(self, kind='poc-verdict'):
        (self.case / 'proof.txt').write_text('{"latency": 8}')
        selected = technical.profile(kind)
        return {'version': '1.0.0', 'case_id': 'alpha-run', 'decision_type': kind,
                'criticality': 'material', 'objective': 'Trial a candidate', 'constraints': ['Measured before adoption'], 'owner': 'CTO review',
                'evidence': [{'id': 'E1', 'ref': 'proof.txt', 'sha256': engine.digest(self.case / 'proof.txt'), 'layer': 'test'}],
                'options': [{'id': 'keep', 'description': 'Keep current', 'tradeoff': 'Known cost'},
                            {'id': 'trial', 'description': 'Trial candidate', 'tradeoff': 'Migration effort'}],
                'assumptions': [{'hypothesis': 'Runtime acceptable', 'falsifier': 'Latency above 10 seconds', 'verification': 'Benchmark'}],
                'sections': [{'id': name, 'analysis': 'Synthetic analysis', 'evidence_refs': ['E1'], 'unknowns': []} for name in selected['required_sections']],
                'measures': [{'id': 'latency', 'value': 8, 'unit': 'seconds', 'status': 'observed', 'evidence_refs': ['E1'],
                              'reading': {'evidence_id': 'E1', 'pointer': '/latency'}}],
                'guardrails': [{'measure_id': 'latency', 'operator': '<=', 'threshold': 10}],
                'decision': {'option_id': 'trial', 'verdict': 'Trial', 'reason': 'Synthetic benchmark', 'next_action': 'Pilot', 'rollback': 'Keep baseline'}}

    def validate(self, memo):
        # Method schemas/profiles are repository-owned; case fixture is isolated.
        return technical.validate(memo, self.case, self.root)

    def test_seven_decision_types_use_one_engine(self):
        for kind in engine.load(ROOT / 'config/technical-decisions.json')['profiles']:
            memo = self.memo(kind)
            result = self.validate(memo)
            self.assertFalse(result['decision_approved'])

    def call(self, memo):
        return self.validate(memo)

    def test_adopt_requires_observed_guardrail(self):
        memo = self.memo()
        memo['decision']['verdict'] = 'Adopt'
        self.assertTrue(self.call(memo)['guardrails_pass'])
        memo['measures'][0]['status'] = 'estimated'
        with self.assertRaisesRegex(ValueError, 'Adopt requires'):
            self.call(memo)

    def test_adopt_rejects_failed_guardrail(self):
        memo = self.memo()
        memo['decision']['verdict'] = 'Adopt'
        memo['guardrails'][0]['threshold'] = 5
        with self.assertRaisesRegex(ValueError, 'Adopt requires'):
            self.call(memo)

    def test_unknown_is_not_numeric(self):
        memo = self.memo()
        memo['measures'][0]['status'] = 'unknown'
        with self.assertRaisesRegex(ValueError, 'Unknown value'):
            self.call(memo)

    def test_required_decision_sections(self):
        memo = self.memo('migration-tco')
        memo['sections'][-1]['id'] = 'wrong-section'
        with self.assertRaisesRegex(ValueError, 'sections missing'):
            self.call(memo)

    def test_critical_decision_needs_adr(self):
        memo = self.memo('rupture-adr')
        memo['criticality'] = 'structural'
        with self.assertRaisesRegex(ValueError, 'ADR evidence'):
            self.call(memo)

    def test_stale_decision_proof(self):
        memo = self.memo()
        (self.case / 'proof.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'evidence changed'):
            self.call(memo)


if __name__ == '__main__':
    unittest.main()
