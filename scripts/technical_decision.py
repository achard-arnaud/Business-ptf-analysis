#!/usr/bin/env python3
"""Decision-specific I/O checks; never asserts that a technical judgement is true."""
import argparse
import importlib.util
import json
from pathlib import Path
from jsonschema import Draft202012Validator

spec = importlib.util.spec_from_file_location('case_io', Path(__file__).with_name('case_runtime.py'))
io = importlib.util.module_from_spec(spec)
spec.loader.exec_module(io)
ROOT = Path(__file__).resolve().parents[1]


def profile(kind, root=ROOT):
    profiles = io.load(root / 'config/technical-decisions.json')['profiles']
    if kind not in profiles:
        raise ValueError('Unknown decision type')
    return profiles[kind]


def validate(memo, case, root=ROOT):
    Draft202012Validator(io.load(root / 'contracts/technical-decision.schema.json')).validate(memo)
    state = io.load(case / 'state.json')
    io.verify(state, case, root)
    if memo['case_id'] != state['case_id']:
        raise ValueError('Decision belongs to a different case')
    selected = profile(memo['decision_type'], root)
    sections = io.unique(memo['sections'])
    if set(sections) != set(selected['required_sections']):
        raise ValueError('Decision-specific sections missing or ambiguous')
    evidence = io.unique(memo['evidence'])
    for item in evidence.values():
        if io.digest(io.local(case, item['ref'])) != item['sha256']:
            raise ValueError('Decision evidence changed')
    for section in sections.values():
        if not set(section['evidence_refs']) <= set(evidence):
            raise ValueError('Unresolved section evidence')
        if not section['evidence_refs'] and not section['unknowns']:
            raise ValueError('Each technical section needs evidence or explicit unknowns')
    measures = io.unique(memo['measures'])
    for measure in measures.values():
        if not set(measure['evidence_refs']) <= set(evidence):
            raise ValueError('Unresolved measure evidence')
        if measure['status'] == 'unknown' and measure['value'] is not None:
            raise ValueError('Unknown value must be null')
        if measure['status'] != 'unknown' and (measure['value'] is None or not measure['evidence_refs']):
            raise ValueError('Measured/estimated value requires numeric value and evidence')
        if measure['status'] == 'observed':
            reading = measure.get('reading')
            if not reading or reading['evidence_id'] not in measure['evidence_refs']:
                raise ValueError('Observed value needs a pinned JSON reading')
            proof = evidence[reading['evidence_id']]
            actual = io.pointer(io.load(io.local(case, proof['ref'])), reading['pointer'])
            if isinstance(actual, bool) or not isinstance(actual, (int, float)) or actual != measure['value']:
                raise ValueError('Observed value differs from recorded measurement')
    checks = []
    for guardrail in memo['guardrails']:
        measure = measures.get(guardrail['measure_id'])
        if measure is None:
            raise ValueError('Guardrail references missing measure')
        value = measure['value']
        passes = value is not None and measure['status'] == 'observed' and (
            value <= guardrail['threshold'] if guardrail['operator'] == '<=' else value >= guardrail['threshold'])
        checks.append(bool(passes))
    options = io.unique(memo['options'])
    if memo['decision']['option_id'] not in options:
        raise ValueError('Decision references unresolved option')
    if memo['decision_type'] == 'poc-verdict' and memo['decision']['verdict'] == 'proposed':
        raise ValueError('PoC requires Adopt/Trial/Hold/Kill')
    if memo['decision']['verdict'] == 'Adopt' and (not checks or not all(checks)):
        raise ValueError('Adopt requires every explicit guardrail to pass on observed measures')
    if memo['criticality'] == 'structural' and not any(e['layer'] == 'adr' for e in evidence.values()):
        raise ValueError('Structural decision requires ADR evidence')
    return {'status': 'decision_contract_valid', 'profile': memo['decision_type'],
            'guardrails_pass': bool(checks) and all(checks), 'technical_truth_verified': False,
            'decision_approved': False}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['profile', 'validate'])
    parser.add_argument('input')
    parser.add_argument('--case')
    args = parser.parse_args()
    try:
        result = profile(args.input) if args.command == 'profile' else validate(
            io.load(args.input), io.case_path(args.case))
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc)}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
