"""Executable boundary tests, including a fresh-case CLI run and stale evidence."""
import copy
import importlib.util
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('case_engine', ROOT / 'scripts/case_runtime.py')
engine = importlib.util.module_from_spec(spec)
spec.loader.exec_module(engine)


class CaseRuntimeTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.addCleanup(self.tmp.cleanup)
        self.root = Path(self.tmp.name)
        for path in ('scripts/case_runtime.py', 'scripts/technical_decision.py',
                     'contracts/case-artifacts.schema.json', 'contracts/technical-decision.schema.json',
                     'config/technical-decisions.json', 'workflow/case-process.json'):
            target = self.root / path
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(ROOT / path, target)
        manifest = engine.load(self.root / 'workflow/case-process.json')
        manifest['templates'] = {'synthetic': {'refs': ['templates/synthetic.md'], 'pages': 3}}
        manifest['stable_refs'] = ['AGENTS.md']
        engine.atomic(self.root / 'workflow/case-process.json', manifest)
        (self.root / 'templates').mkdir()
        (self.root / 'templates/synthetic.md').write_text('Synthetic template')
        (self.root / 'AGENTS.md').write_text('Synthetic instructions')
        engine.atomic(self.root / 'workflow/engine-release.json', {'version': engine.ENGINE_VERSION,
            'files': {p: engine.digest(self.root / p) for p in ['scripts/case_runtime.py', 'scripts/technical_decision.py',
              'contracts/case-artifacts.schema.json', 'contracts/technical-decision.schema.json', 'config/technical-decisions.json']}})
        self.intake = {'entity_id': 'alpha', 'objective': 'Decide a pilot', 'constraints': ['No approval inferred'],
                       'cutoff': '2026-11-17', 'template_id': 'synthetic', 'render_requested': False}
        engine.init('alpha-run', self.intake, self.root)
        self.case = self.root / 'data/cases/alpha-run'

    def result(self, stage, content):
        packet = engine.begin('alpha-run', stage, 'test_agent', self.root)
        artifact = {'case_id': 'alpha-run', 'kind': {'A0': 'evidence', 'A1': 'graph', 'A2': 'scaffold', 'A3': 'composition', 'A4': 'review'}[stage], **content}
        engine.atomic(self.case / packet['output_ref'], artifact)
        return packet

    def evidence(self):
        packet = self.result('A0', {'sources': [{'id': 'S1', 'url': 'https://example.org/source', 'locator': 'p. 1',
                            'fetched_at': '2026-11-17T00:00:00Z', 'coverage': 'read',
                            'capture_ref': 'stages/A0/attempt-1/capture.txt'}], 'unknowns': ['Internal economics']})
        (self.case / 'stages/A0/attempt-1/capture.txt').write_text('Synthetic observed evidence')
        engine.complete('alpha-run', 'A0', self.root)
        return packet

    def graph(self):
        return {'nodes': [{'id': 'SN1', 'type': 'source', 'source_id': 'S1'},
                          {'id': 'F1', 'type': 'fragment', 'locator': 'p. 1', 'text': 'Synthetic', 'evidence_status': 'verified'},
                          {'id': 'C1', 'type': 'claim', 'statement': 'Synthetic fact', 'status': 'fact'}],
                'edges': [{'from': 'F1', 'to': 'SN1', 'type': 'extracted_from'}, {'from': 'F1', 'to': 'C1', 'type': 'supports'}], 'unknowns': []}

    def through_scaffold(self):
        self.evidence()
        self.result('A1', self.graph())
        engine.complete('alpha-run', 'A1', self.root)
        self.result('A2', {'decision': 'Trial', 'strongest_objection': 'Unknown value', 'falsifier': 'No benefit measured',
                          'sections': [{'id': 'SEC1', 'action_title': 'Trial before scale', 'claim_ids': ['C1']}]})
        engine.complete('alpha-run', 'A2', self.root)

    def test_init_creates_graph_first_and_refuses_reuse(self):
        state = engine.load(self.case / 'state.json')
        self.assertEqual(engine.load(self.case / 'graph.json')['nodes'], [])
        self.assertTrue(state['events'][0]['graph_created_before_collection'])
        with self.assertRaises(FileExistsError):
            engine.init('alpha-run', self.intake, self.root)

    def test_stage_cannot_skip_dependencies(self):
        with self.assertRaisesRegex(ValueError, 'dependency'):
            engine.begin('alpha-run', 'A3', 'test', self.root)

    def test_manifest_cannot_weaken_stage_chain(self):
        manifest = engine.load(self.root / 'workflow/case-process.json')
        manifest['stages'][-1]['depends_on'] = []
        engine.atomic(self.root / 'workflow/case-process.json', manifest)
        with self.assertRaisesRegex(ValueError, 'dependency contract weakened'):
            engine.process(self.root)

    def test_capture_tampering_blocks_resume(self):
        self.evidence()
        (self.case / 'stages/A0/attempt-1/capture.txt').write_text('Changed')
        with self.assertRaisesRegex(ValueError, 'Stale context'):
            engine.inspect('alpha-run', self.root)

    def test_build_pin_drift_blocks_resume(self):
        (self.root / 'AGENTS.md').write_text('new BUILD')
        with self.assertRaisesRegex(ValueError, 'Stale context'):
            engine.inspect('alpha-run', self.root)

    def test_context_packet_tampering(self):
        p = engine.begin('alpha-run', 'A0', 'test', self.root)
        engine.atomic(self.case / 'stages/A0/attempt-1/context.json', {**p, 'actor': 'replacement'})
        with self.assertRaisesRegex(ValueError, 'Stale context'):
            engine.inspect('alpha-run', self.root)

    def test_intake_tampering(self):
        engine.atomic(self.case / 'intake.json', {**self.intake, 'entity_id': 'beta'})
        with self.assertRaisesRegex(ValueError, 'Stale intake'):
            engine.inspect('alpha-run', self.root)

    def test_typed_graph_and_provenance(self):
        self.evidence()
        g = self.graph()
        g['edges'][0]['from'] = 'C1'
        self.result('A1', g)
        with self.assertRaisesRegex(ValueError, 'typed edge'):
            engine.complete('alpha-run', 'A1', self.root)
        self.assertEqual(engine.load(self.case / 'state.json')['events'][-1]['action'], 'stage_rejected')

    def test_vendor_claim_is_not_verified_fact(self):
        self.evidence()
        g = self.graph()
        g['nodes'][1]['evidence_status'] = 'attributed'
        self.result('A1', g)
        with self.assertRaisesRegex(ValueError, 'Fact requires'):
            engine.complete('alpha-run', 'A1', self.root)

    def test_foreign_artifact_ref_is_rejected(self):
        p = self.result('A0', {'sources': [{'id': 'S1', 'url': 'https://example.org', 'locator': 'p1',
                     'fetched_at': '2026-11-17T00:00:00Z', 'coverage': 'read', 'capture_ref': '../../escape'}], 'unknowns': []})
        with self.assertRaisesRegex(ValueError, 'Unsafe'):
            engine.complete('alpha-run', 'A0', self.root)

    def test_cross_attempt_reference_is_rejected(self):
        self.evidence()
        engine.invalidate('alpha-run', 'A0', 'Refresh evidence', self.root)
        self.result('A0', {'sources': [{'id': 'S1', 'url': 'https://example.org', 'locator': 'p1',
                     'fetched_at': '2026-11-17T00:00:00Z', 'coverage': 'read', 'capture_ref': 'stages/A0/attempt-1/capture.txt'}], 'unknowns': []})
        with self.assertRaisesRegex(ValueError, 'another attempt'):
            engine.complete('alpha-run', 'A0', self.root)

    def test_composition_preserves_claim_mapping(self):
        self.through_scaffold()
        self.result('A3', {'sections': [{'id': 'SEC1', 'prose': 'Trial', 'claim_ids': ['missing']}]})
        with self.assertRaisesRegex(ValueError, 'unresolved claim'):
            engine.complete('alpha-run', 'A3', self.root)

    def test_explicit_prose_citation_cannot_escape_mapping(self):
        self.evidence()
        graph = self.graph()
        graph['nodes'].append({'id': 'C2', 'type': 'claim', 'statement': 'Unrelated unknown', 'status': 'unknown'})
        self.result('A1', graph)
        engine.complete('alpha-run', 'A1', self.root)
        self.result('A2', {'decision': 'Trial', 'strongest_objection': 'Unknown', 'falsifier': 'No gain',
             'sections': [{'id': 'SEC1', 'action_title': 'Trial', 'claim_ids': ['C1']}]})
        engine.complete('alpha-run', 'A2', self.root)
        self.result('A3', {'sections': [{'id': 'SEC1', 'prose': 'Unmapped assertion (C2).', 'claim_ids': ['C1']}]})
        with self.assertRaisesRegex(ValueError, 'outside its section mapping'):
            engine.complete('alpha-run', 'A3', self.root)

    def test_runtime_version_drift_blocks_resume(self):
        state = engine.load(self.case / 'state.json')
        state['runtime']['packages']['jsonschema'] = '0.0.0'
        engine.atomic(self.case / 'state.json', state)
        with self.assertRaisesRegex(ValueError, 'python_or_dependency'):
            engine.inspect('alpha-run', self.root)

    def test_invalidation_preserves_evidence_and_attempts(self):
        self.through_scaffold()
        before = (self.case / 'stages/A1/attempt-1/result.json').read_bytes()
        r = engine.invalidate('alpha-run', 'A1', 'Targeted correction', self.root)
        self.assertEqual(r['invalidated'], ['A1', 'A2', 'A3', 'A4'])
        self.assertEqual((self.case / 'stages/A1/attempt-1/result.json').read_bytes(), before)
        state = engine.load(self.case / 'state.json')
        self.assertEqual(state['stages']['A0']['status'], 'passed')
        self.assertEqual(engine.begin('alpha-run', 'A1', 'test', self.root)['attempt'], 2)

    def test_complete_chain_logs_calls_but_never_business_approval(self):
        self.through_scaffold()
        self.result('A3', {'sections': [{'id': 'SEC1', 'prose': 'Trial after measuring', 'claim_ids': ['C1']}]})
        engine.complete('alpha-run', 'A3', self.root)
        self.result('A4', {'reviews': [{'lens': lens, 'verdict': 'pass', 'reviewer': 'test_agent',
                     'evidence_ref': f'stages/A4/attempt-1/{i}.md'} for i, lens in enumerate(['evidence', 'counter-perspective', 'decision'])]})
        for i in range(3):
            (self.case / f'stages/A4/attempt-1/{i}.md').write_text('Synthetic review; no business approval')
        engine.complete('alpha-run', 'A4', self.root)
        state = engine.inspect('alpha-run', self.root)
        self.assertFalse(state['business_approval'])
        self.assertEqual({v['status'] for v in state['stages'].values()}, {'passed'})
        self.assertEqual(len(engine.load(self.case / 'state.json')['events']), 11)

    def test_cli_is_an_executed_consumer(self):
        cli = self.root / 'scripts/case_runtime.py'
        result = subprocess.run([sys.executable, str(cli), 'status', '--case', 'alpha-run'], capture_output=True, text=True)
        self.assertEqual(result.returncode, 0, result.stdout)
        self.assertEqual(json.loads(result.stdout)['case_id'], 'alpha-run')
        result = subprocess.run([sys.executable, str(cli), 'begin', '--case', 'alpha-run', '--stage', 'A4'], capture_output=True, text=True)
        self.assertNotEqual(result.returncode, 0)

    def prepare_render(self):
        manifest = engine.load(self.root / 'workflow/case-process.json')
        renderer = self.root / 'renderer.py'
        renderer.write_text('''import json,sys
from pathlib import Path
from pypdf import PdfWriter
out=Path(sys.argv[2]);pdf=PdfWriter()
for _ in range(3):pdf.add_blank_page(400,300)
with (out/'output.pdf').open('wb') as f:pdf.write(f)
(out/'qa.json').write_text(json.dumps({'pass':True,'page_count':3,'summary':{'overflows':0,'overlaps':0}}))
''')
        engine.atomic(self.root / 'payload.schema.json', {'type': 'object', 'required': ['entity_id']})
        manifest['templates']['synthetic'].update(renderer={'entrypoint': 'renderer.py', 'args': []}, payload_schema='payload.schema.json')
        manifest['templates']['synthetic']['refs'] += ['renderer.py', 'payload.schema.json']
        engine.atomic(self.root / 'workflow/case-process.json', manifest)
        # Replace only the unused synthetic setUp fixture with a fresh render fixture.
        self.intake['render_requested'] = True
        shutil.rmtree(self.case)
        engine.init('alpha-run', self.intake, self.root)
        self.through_scaffold()
        packet = self.result('A3', {'sections': [{'id': 'SEC1', 'prose': 'Trial', 'claim_ids': ['C1']}],
                                   'payload_ref': 'stages/A3/attempt-1/payload.json'})
        engine.atomic(self.case / 'stages/A3/attempt-1/payload.json', {'entity_id': 'alpha'})
        engine.complete('alpha-run', 'A3', self.root)
        engine.begin('alpha-run', 'A4', 'test', self.root)

    def test_real_renderer_call_is_logged_and_receipt_bound(self):
        self.prepare_render()
        receipt = engine.render('alpha-run', self.root)
        self.assertEqual(receipt['page_count'], 3)
        self.assertEqual(engine.load(self.case / 'state.json')['events'][-1]['action'], 'render_completed')
        qa = self.case / 'stages/A4/attempt-1/render-1/qa.json'
        qa.write_text('{"pass": false}')
        with self.assertRaisesRegex(ValueError, 'Stale context'):
            engine.inspect('alpha-run', self.root)

    def test_manual_render_receipt_without_call_is_rejected(self):
        self.prepare_render()
        state = engine.load(self.case / 'state.json')
        artifact = {'case_id': 'alpha-run', 'kind': 'review', 'reviews': [
            {'lens': lens, 'verdict': 'pass', 'reviewer': 'test', 'evidence_ref': f'stages/A4/attempt-1/{i}.md'}
            for i, lens in enumerate(['evidence', 'counter-perspective', 'decision'])],
            'render': {'qa_status': 'pass', 'page_count': 3, 'files': {'a.pdf': 'a'*64, 'qa.json': 'b'*64}, 'reviewer': 'self-declared'}}
        with self.assertRaisesRegex(ValueError, 'not produced by the stage render call'):
            engine.semantic(artifact, state, self.case, self.root)

    def proposal(self):
        (self.case / 'observation.txt').write_text('Synthetic failure')
        (self.root / 'adr.md').write_text('Synthetic ADR')
        return {'version': '1.0.0', 'case_id': 'alpha-run', 'state_sha256': engine.digest(self.case / 'state.json'),
                'axis': 'ci', 'action': 'no_change', 'objective': 'Explain missing oracle', 'constraints': ['No fake values'],
                'observation': 'Synthetic failure', 'cause_status': 'unknown', 'adr_refs': ['adr.md'],
                'adr_disposition': 'unknown', 'issue_ref': 'https://example.org/issue',
                'evidence': [{'ref': 'observation.txt', 'sha256': engine.digest(self.case / 'observation.txt')}],
                'metrics': [], 'experiment': None}

    def test_loopback_does_not_mutate_run(self):
        proposal = self.proposal()
        engine.atomic(self.case / 'proposal.json', proposal)
        before = (self.case / 'state.json').read_bytes()
        result = engine.loopback('alpha-run', 'proposal.json', self.root)
        self.assertFalse(result['run_mutated'])
        self.assertEqual((self.case / 'state.json').read_bytes(), before)

    def test_loopback_rejects_stale_evidence(self):
        proposal = self.proposal()
        engine.atomic(self.case / 'proposal.json', proposal)
        (self.case / 'observation.txt').write_text('changed')
        with self.assertRaisesRegex(ValueError, 'evidence changed'):
            engine.loopback('alpha-run', 'proposal.json', self.root)

    def test_loopback_rejects_invented_measurement(self):
        proposal = self.proposal()
        proposal['metrics'] = [{'name': 'time', 'unit': 'seconds', 'status': 'unknown', 'before': 5, 'after': 2, 'evidence_refs': []}]
        engine.atomic(self.case / 'proposal.json', proposal)
        with self.assertRaisesRegex(ValueError, 'invent'):
            engine.loopback('alpha-run', 'proposal.json', self.root)

    def test_loopback_observed_values_are_read_from_hashed_proof(self):
        proposal = self.proposal()
        engine.atomic(self.case / 'measurements.json', {'before': 1, 'after': 0})
        proposal['evidence'].append({'ref': 'measurements.json', 'sha256': engine.digest(self.case / 'measurements.json')})
        proposal['metrics'] = [{'name': 'overflows', 'unit': 'findings', 'status': 'observed',
             'before': 1, 'after': 0, 'evidence_refs': ['measurements.json'],
             'before_reading': {'ref': 'measurements.json', 'pointer': '/before'},
             'after_reading': {'ref': 'measurements.json', 'pointer': '/after'}}]
        engine.atomic(self.case / 'proposal.json', proposal)
        self.assertEqual(engine.loopback('alpha-run', 'proposal.json', self.root)['status'], 'proposal_validated_not_applied')
        proposal['metrics'][0]['after'] = -1
        engine.atomic(self.case / 'proposal.json', proposal)
        with self.assertRaisesRegex(ValueError, 'differs from recorded'):
            engine.loopback('alpha-run', 'proposal.json', self.root)


if __name__ == '__main__':
    unittest.main()
