#!/usr/bin/env python3
"""Versioned manual-agent stage boundary. No research, model calls or BUILD writes.

The recorded actor and reviews are declarations; hashes attest bytes, not truth.
All mutations serialize on the case lock; state.json owns the append-only event list.
"""
import argparse
import copy
import fcntl
import hashlib
import importlib.util
import json
import os
import re
import sys
import subprocess
import tempfile
from importlib import metadata
from contextlib import contextmanager
from datetime import datetime, timezone
from pathlib import Path

from jsonschema import Draft202012Validator, FormatChecker
from jsonschema.exceptions import ValidationError

ROOT = Path(__file__).resolve().parents[1]
PROCESS = 'workflow/case-process.json'
SCHEMA = 'contracts/case-artifacts.schema.json'
ENGINE_VERSION = '1.0.0'


def now():
    return datetime.now(timezone.utc).isoformat()


def runtime_fingerprint():
    return {'python': sys.version.split()[0],
            'packages': {name: metadata.version(name) for name in ('jsonschema', 'pypdf')}}


def load(path):
    return json.loads(Path(path).read_text(encoding='utf-8'))


def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def pointer(document, path):
    if not isinstance(path, str) or not path.startswith('/'):
        raise ValueError('Measurement requires JSON pointer')
    for part in path[1:].split('/'):
        key = part.replace('~1', '/').replace('~0', '~')
        document = document[int(key)] if isinstance(document, list) else document[key]
    return document


def identity(value):
    if not isinstance(value, str) or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', value):
        raise ValueError('Expected a lowercase slug')
    return value


def local(root, relative, exists=True):
    if (not isinstance(relative, str) or not relative or '\\' in relative
            or Path(relative).is_absolute() or any(x in {'..', '.git'} for x in relative.split('/'))):
        raise ValueError('Unsafe local reference')
    root = Path(root).resolve()
    target = (root / relative).resolve()
    if not target.is_relative_to(root) or (exists and not target.is_file()):
        raise ValueError('Missing or escaped reference: ' + relative)
    return target


def atomic(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp = tempfile.mkstemp(prefix='.case-', dir=path.parent)
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as stream:
            json.dump(data, stream, ensure_ascii=False, indent=2)
            stream.write('\n')
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(tmp, path)
    finally:
        if os.path.exists(tmp):
            os.unlink(tmp)


def schema_check(data, definition, root=ROOT):
    schema = load(local(root, SCHEMA))
    Draft202012Validator({'$ref': '#/$defs/' + definition, '$defs': schema['$defs']},
                        format_checker=FormatChecker()).validate(data)


def process(root=ROOT):
    spec = load(local(root, PROCESS))
    if spec['version'] != ENGINE_VERSION or spec['executor'] != 'manual_agent':
        raise ValueError('Unsupported process version/executor')
    stages = spec['stages']
    if not stages or len({s['id'] for s in stages}) != len(stages):
        raise ValueError('Duplicate or empty stage manifest')
    seen = set()
    for stage in stages:
        identity(stage['kind'])
        if not set(stage['depends_on']) <= seen:
            raise ValueError('Process must be topologically ordered')
        seen.add(stage['id'])
    expected = {'A0': 'evidence', 'A1': 'graph', 'A2': 'scaffold', 'A3': 'composition', 'A4': 'review'}
    if {s['id']: s['kind'] for s in stages} != expected:
        raise ValueError('Stage roles incompatible with engine version')
    ancestors = {}
    required = {'A0': set(), 'A1': {'A0'}, 'A2': {'A1'}, 'A3': {'A1', 'A2'}, 'A4': {'A0', 'A1', 'A2', 'A3'}}
    for stage in stages:
        inherited = set(stage['depends_on'])
        for dependency in stage['depends_on']:
            inherited.update(ancestors[dependency])
        if not required[stage['id']] <= inherited:
            raise ValueError('Stage dependency contract weakened')
        ancestors[stage['id']] = inherited
    return spec


def check_contracts(root=ROOT):
    spec = process(root)
    schemas = load(local(root, SCHEMA))
    Draft202012Validator.check_schema(schemas)
    expected = {'A0': 'evidence', 'A1': 'graph', 'A2': 'scaffold', 'A3': 'composition', 'A4': 'review'}
    if {s['id']: s['kind'] for s in spec['stages']} != expected:
        raise ValueError('Stage roles incompatible with engine version')
    for ref in spec['stable_refs']:
        local(root, ref)
    for profile in spec['templates'].values():
        for ref in profile['refs']:
            local(root, ref)
    release = load(local(root, 'workflow/engine-release.json'))
    required_files = {'scripts/case_runtime.py', 'scripts/technical_decision.py', SCHEMA,
                      'contracts/technical-decision.schema.json', 'config/technical-decisions.json'}
    if release.get('version') != ENGINE_VERSION or set(release['files']) != required_files:
        raise ValueError('Incomplete engine release inventory')
    for ref, sha in release['files'].items():
        if digest(local(root, ref)) != sha:
            raise ValueError('Engine release hash mismatch: ' + ref)
    return {'status': 'contracts_pass', 'engine_version': ENGINE_VERSION, 'templates': len(spec['templates'])}


def case_path(case_id, root=ROOT):
    return local(root, 'data/cases/' + identity(case_id), exists=False)


@contextmanager
def locked(case):
    if not (case / 'state.json').is_file():
        raise ValueError('Unknown case')
    with (case / '.lock').open('a') as stream:
        fcntl.flock(stream, fcntl.LOCK_EX)
        yield


def event(state, action, **fields):
    state['revision'] += 1
    state['events'].append({'sequence': state['revision'], 'at': now(), 'action': action, **fields})


def init(case_id, intake, root=ROOT):
    check_contracts(root)
    spec = process(root)
    schema_check(intake, 'intake', root)
    template = intake['template_id']
    if template not in spec['templates']:
        raise ValueError('Unknown template; no silent fallback')
    profile = spec['templates'][template]
    if intake.get('decision_type'):
        registry = load(local(root, 'config/technical-decisions.json'))['profiles']
        if intake['decision_type'] not in registry:
            raise ValueError('Unknown technical decision profile')
    refs = [PROCESS, SCHEMA, 'scripts/case_runtime.py', *spec['stable_refs'], *profile['refs']]
    pins = {p: digest(local(root, p)) for p in sorted(set(refs))}
    case = case_path(case_id, root)
    case.parent.mkdir(parents=True, exist_ok=True)
    case.mkdir()  # Refuse existing instance, including concurrent initialization.
    state = {'version': ENGINE_VERSION, 'case_id': case_id, 'revision': 0, 'intake': intake,
             'build_pins': pins, 'profile': profile, 'stages': {}, 'events': [],
             'runtime': runtime_fingerprint(), 'business_approval': False}
    for stage in spec['stages']:
        state['stages'][stage['id']] = {'status': 'pending', 'attempt': 0}
    atomic(case / 'intake.json', intake)
    state['intake_sha256'] = digest(case / 'intake.json')
    atomic(case / 'graph.json', {'case_id': case_id, 'nodes': [], 'edges': []})
    state['graph_ref'] = 'graph.json'
    event(state, 'initialized', graph_created_before_collection=True)
    atomic(case / 'state.json', state)
    return state


def verify(state, case, root=ROOT, allow_stale=False):
    if state['case_id'] != case.name or state['version'] != ENGINE_VERSION:
        raise ValueError('Case identity/version mismatch')
    if digest(local(case, 'intake.json')) != state['intake_sha256'] or load(case / 'intake.json') != state['intake']:
        raise ValueError('Stale intake')
    if len(state['events']) != state['revision'] or [e['sequence'] for e in state['events']] != list(range(1, state['revision'] + 1)):
        raise ValueError('Corrupt execution event sequence')
    def changed(base, ref, sha):
        try:
            return digest(local(base, ref)) != sha
        except (OSError, ValueError):
            return True
    stale = [p for p, sha in state['build_pins'].items() if changed(root, p, sha)]
    if state['runtime'] != runtime_fingerprint():
        stale.append('runtime:python_or_dependency_version_changed')
    for stage, record in state['stages'].items():
        if record['status'] not in {'running', 'passed'}:
            continue
        refs = dict(record.get('context_pins', {}))
        refs.update(record.get('output_pins', {}))
        for ref, sha in refs.items():
            if changed(case, ref, sha):
                stale.append(stage + ':' + ref)
    if stale and not allow_stale:
        raise ValueError('Stale context: ' + ', '.join(stale))
    return stale


def rules(spec, stage):
    found = [s for s in spec['stages'] if s['id'] == stage]
    if not found:
        raise ValueError('Unknown stage')
    return found[0]


def begin(case_id, stage, actor, root=ROOT):
    if not isinstance(actor, str) or not actor.strip():
        raise ValueError('Stage actor required')
    case = case_path(case_id, root)
    with locked(case):
        state = load(case / 'state.json')
        verify(state, case, root)
        rule = rules(process(root), stage)
        record = state['stages'][stage]
        if record['status'] != 'pending':
            raise ValueError('Stage already running/passed; invalidate explicitly')
        if any(state['stages'][d]['status'] != 'passed' for d in rule['depends_on']):
            raise ValueError('Unmet stage dependency')
        record['attempt'] += 1
        relative = f'stages/{stage}/attempt-{record["attempt"]}'
        directory = local(case, relative, exists=False)
        directory.mkdir(parents=True, exist_ok=False)
        inputs = {}
        for dependency in rule['depends_on']:
            inputs.update(state['stages'][dependency]['output_pins'])
        inputs['intake.json'] = state['intake_sha256']
        packet = {'version': ENGINE_VERSION, 'case_id': case_id, 'stage': stage,
                  'attempt': record['attempt'], 'actor': actor, 'build_pins': state['build_pins'],
                  'input_pins': inputs, 'output_schema': SCHEMA + '#/$defs/' + rule['kind'],
                  'output_ref': relative + '/result.json', 'instructions': rule['instructions'],
                  'template_profile': state['profile'], 'usage': {'provider_tokens': None}}
        atomic(directory / 'context.json', packet)
        record.update(status='running', directory=relative, actor=actor,
                      context_pins={**inputs, relative + '/context.json': digest(directory / 'context.json')})
        event(state, 'stage_started', stage=stage, attempt=record['attempt'], actor=actor)
        atomic(case / 'state.json', state)
        return packet


def current_artifact(state, case, stage):
    record = state['stages'][stage]
    if record['status'] != 'passed':
        raise ValueError('Unpassed stage: ' + stage)
    return load(local(case, record['directory'] + '/result.json'))


def unique(rows):
    result = {r['id']: r for r in rows}
    if len(result) != len(rows):
        raise ValueError('Duplicate node/source/section ID')
    return result


def semantic(artifact, state, case, root=ROOT):
    kind = artifact['kind']
    if kind == 'evidence':
        sources = unique(artifact['sources'])
        refs = []
        for source in sources.values():
            refs.append(source['capture_ref'])
        return refs
    if kind == 'graph':
        sources = unique(current_artifact(state, case, 'A0')['sources'])
        nodes = unique(artifact['nodes'])
        edges = artifact['edges']
        shapes = {'extracted_from': ({'fragment'}, {'source'}),
                  'supports': ({'fragment', 'claim'}, {'claim'}),
                  'contradicts': ({'claim'}, {'claim'}),
                  'depends_on': ({'claim'}, {'claim'})}
        for n in nodes.values():
            if n['type'] == 'source' and n['source_id'] not in sources:
                raise ValueError('Unresolved source')
        for e in edges:
            if e['from'] not in nodes or e['to'] not in nodes or e['from'] == e['to']:
                raise ValueError('Dangling/self graph edge')
            left, right = shapes[e['type']]
            if nodes[e['from']]['type'] not in left or nodes[e['to']]['type'] not in right:
                raise ValueError('Invalid typed edge endpoints')
        for node in nodes.values():
            if node['type'] == 'fragment':
                provenance = [nodes[e['to']] for e in edges if e['from'] == node['id'] and e['type'] == 'extracted_from']
                if not provenance or any(sources[s['source_id']]['coverage'] != 'read' for s in provenance):
                    raise ValueError('Fragment without read source provenance')
            if node['type'] == 'claim' and node['status'] in {'fact', 'attributed_claim', 'inference'}:
                support = [nodes[e['from']] for e in edges if e['to'] == node['id'] and e['type'] == 'supports']
                if not any(n['type'] == 'fragment' for n in support):
                    raise ValueError('Material claim without fragment support')
                if node['status'] == 'fact' and any(n.get('evidence_status') != 'verified' for n in support if n['type'] == 'fragment'):
                    raise ValueError('Fact requires verified fragment; use attributed_claim')
        # Only depends_on is a DAG. Contradictions/support need not be acyclic.
        def visit(key, trail):
            if key in trail:
                raise ValueError('Dependency graph cycle')
            for e in edges:
                if e['from'] == key and e['type'] == 'depends_on':
                    visit(e['to'], trail | {key})
        for key in nodes:
            visit(key, set())
    elif kind in {'scaffold', 'composition'}:
        graph = current_artifact(state, case, 'A1')
        claims = {n['id'] for n in graph['nodes'] if n['type'] == 'claim'}
        unique(artifact['sections'])
        for section in artifact['sections']:
            if not set(section['claim_ids']) <= claims:
                raise ValueError('Section references unresolved claim')
        if kind == 'composition':
            scaffold = unique(current_artifact(state, case, 'A2')['sections'])
            if set(scaffold) != {s['id'] for s in artifact['sections']}:
                raise ValueError('Composition/scaffold section mismatch')
            for section in artifact['sections']:
                if section['claim_ids'] != scaffold[section['id']]['claim_ids']:
                    raise ValueError('Composition changed approved claim mapping; revise scaffold')
                explicit = {claim for claim in claims if re.search(r'(?<![\w-])' + re.escape(claim) + r'(?![\w-])', section['prose'])}
                if not explicit <= set(section['claim_ids']):
                    raise ValueError('Prose cites a claim outside its section mapping')
            if state['intake']['render_requested']:
                profile = state['profile']
                if not profile.get('renderer') or not profile.get('payload_schema'):
                    raise ValueError('Selected template has no executable render adapter')
                payload_ref = artifact.get('payload_ref')
                payload = load(local(case, payload_ref))
                Draft202012Validator(load(local(root, profile['payload_schema']))).validate(payload)
                if payload.get('entity_id') != state['intake']['entity_id']:
                    raise ValueError('Render payload entity does not match intake')
                return [payload_ref]
        elif state['intake'].get('decision_type'):
            memo_ref = artifact.get('decision_memo_ref')
            memo = load(local(case, memo_ref))
            if memo['decision_type'] != state['intake']['decision_type']:
                raise ValueError('Technical memo differs from selected intake decision profile')
            module_spec = importlib.util.spec_from_file_location('stage_decision_io', local(root, 'scripts/technical_decision.py'))
            module = importlib.util.module_from_spec(module_spec)
            module_spec.loader.exec_module(module)
            module.validate(memo, case, root)
            if artifact['decision'] != memo['decision']['verdict']:
                raise ValueError('Scaffold decision differs from validated technical verdict')
            return [memo_ref, *[item['ref'] for item in memo['evidence']]]
    elif kind == 'review':
        if any(r['verdict'] != 'pass' for r in artifact['reviews']):
            raise ValueError('Review has unresolved findings')
        if {r['lens'] for r in artifact['reviews']} != {'evidence', 'counter-perspective', 'decision'} or len(artifact['reviews']) != 3:
            raise ValueError('Three distinct reviews required')
        refs = [r['evidence_ref'] for r in artifact['reviews']]
        if state['intake']['render_requested']:
            receipt = artifact.get('render')
            if receipt != state['stages']['A4'].get('render_receipt'):
                raise ValueError('Render receipt was not produced by the stage render call')
            if not receipt or receipt['qa_status'] != 'pass':
                raise ValueError('Actual render receipt required')
            if receipt['page_count'] != state['profile']['pages'] and state['profile']['pages'] is not None:
                raise ValueError('Wrong physical page count')
            refs += list(receipt['files'])
            for ref, sha in receipt['files'].items():
                if digest(local(case, ref)) != sha:
                    raise ValueError('Stale render file')
            from pypdf import PdfReader
            pdfs = [r for r in receipt['files'] if r.endswith('.pdf')]
            qa_refs = [r for r in receipt['files'] if r.endswith('qa.json')]
            if len(pdfs) != 1 or len(qa_refs) != 1:
                raise ValueError('Render requires one physical PDF and one qa.json')
            if len(PdfReader(local(case, pdfs[0])).pages) != receipt['page_count']:
                raise ValueError('PDF physical pages differ from receipt')
            qa = load(local(case, qa_refs[0]))
            if qa.get('pass') is not True or qa.get('page_count') != receipt['page_count']:
                raise ValueError('Rendered QA failed or page count differs')
            if not qa.get('summary') or any(value != 0 for value in qa['summary'].values()):
                raise ValueError('Rendered QA reports findings')
        return refs
    return []


def complete(case_id, stage, root=ROOT):
    case = case_path(case_id, root)
    with locked(case):
        state = load(case / 'state.json')
        verify(state, case, root)
        record = state['stages'][stage]
        if record['status'] != 'running':
            raise ValueError('Stage has not begun')
        ref = record['directory'] + '/result.json'
        try:
            artifact = load(local(case, ref))
            rule = rules(process(root), stage)
            schema_check(artifact, rule['kind'], root)
            if artifact['case_id'] != case_id or artifact['kind'] != rule['kind']:
                raise ValueError('Artifact identity/kind mismatch')
            refs = semantic(artifact, state, case, root)
            # References must be owned by this attempt; inputs are already pinned separately.
            for path in refs:
                if (not local(case, path).is_relative_to(local(case, record['directory'], exists=False))
                        and path not in record['context_pins']):
                    raise ValueError('Output evidence belongs to another attempt')
            pins = {p: digest(local(case, p)) for p in [ref, *refs]}
            record.update(status='passed', output_pins=pins)
            if stage == 'A1':
                state['graph_ref'] = ref
            event(state, 'stage_completed', stage=stage, attempt=record['attempt'], output_pins=pins,
                  check='structural_and_reference_integrity', semantic_truth_verified=False)
        except (ValueError, OSError, KeyError, TypeError, ValidationError) as exc:
            event(state, 'stage_rejected', stage=stage, reason=str(exc)[:500])
            atomic(case / 'state.json', state)
            raise
        atomic(case / 'state.json', state)
        return {'status': 'passed', 'stage': stage, 'business_approval': False}


def invalidate(case_id, stage, reason, root=ROOT):
    if not reason.strip():
        raise ValueError('Invalidation reason required')
    case = case_path(case_id, root)
    with locked(case):
        state = load(case / 'state.json')
        spec = process(root)
        rules(spec, stage)
        affected = {stage}
        for rule in spec['stages']:
            if affected.intersection(rule['depends_on']):
                affected.add(rule['id'])
        for key in affected:
            old = state['stages'][key]
            # Historical attempt files and events are retained.
            state['stages'][key] = {'status': 'pending', 'attempt': old['attempt']}
        if 'A1' in affected:
            state['graph_ref'] = 'graph.json'
        event(state, 'invalidated', stages=sorted(affected), reason=reason)
        atomic(case / 'state.json', state)
        return {'invalidated': sorted(affected), 'build_pins_changed': False}


def inspect(case_id, root=ROOT):
    case = case_path(case_id, root)
    with locked(case):
        state = load(case / 'state.json')
        verify(state, case, root)
        return {'case_id': case_id, 'revision': state['revision'], 'stages': state['stages'],
                'business_approval': False, 'provider_usage': 'unknown'}


def render(case_id, root=ROOT):
    """Invoke the selected repository renderer and retain its real receipts/logs."""
    from pypdf import PdfReader
    case = case_path(case_id, root)
    with locked(case):
        state = load(case / 'state.json')
        verify(state, case, root)
        record = state['stages']['A4']
        if record['status'] != 'running' or not state['intake']['render_requested']:
            raise ValueError('Render requires a running A4 and an explicit render request')
        profile = state['profile']
        adapter = profile.get('renderer')
        if not adapter or adapter['entrypoint'] not in state['build_pins']:
            raise ValueError('No pinned executable render adapter')
        composition = current_artifact(state, case, 'A3')
        payload = local(case, composition['payload_ref'])
        attempt = record.get('render_attempt', 0) + 1
        record['render_attempt'] = attempt
        record.pop('render_receipt', None)
        relative = record['directory'] + '/render-' + str(attempt)
        out = local(case, relative, exists=False)
        out.mkdir()
        command = [sys.executable, str(local(root, adapter['entrypoint'])), str(payload), str(out), *adapter['args']]
        event(state, 'render_started', stage='A4', render_attempt=attempt, command=command)
        atomic(case / 'state.json', state)
        try:
            done = subprocess.run(command, capture_output=True, text=True, timeout=120, check=False)
            (out / 'renderer.log').write_text(done.stdout + done.stderr, encoding='utf-8')
            if done.returncode:
                raise ValueError('Renderer failed; see ' + relative + '/renderer.log')
            qa = load(local(out, 'qa.json'))
            pdfs = list(out.glob('*.pdf'))
            if len(pdfs) != 1 or qa.get('pass') is not True or not qa.get('summary') or any(qa['summary'].values()):
                raise ValueError('Renderer output/QA rejected')
            pages = len(PdfReader(pdfs[0]).pages)
            if pages != qa['page_count'] or (profile['pages'] is not None and pages != profile['pages']):
                raise ValueError('Renderer physical page count rejected')
            files = {f.relative_to(case).as_posix(): digest(f) for f in out.iterdir() if f.is_file()}
            receipt = {'qa_status': 'pass', 'page_count': pages, 'files': files, 'reviewer': 'render_adapter'}
            record['render_receipt'] = receipt
            record['context_pins'].update(files)
            event(state, 'render_completed', stage='A4', render_attempt=attempt,
                  payload_sha256=digest(payload), renderer_sha256=digest(local(root, adapter['entrypoint'])), files=files)
        except Exception as exc:
            event(state, 'render_rejected', stage='A4', render_attempt=attempt, reason=str(exc)[:500])
            atomic(case / 'state.json', state)
            raise
        atomic(case / 'state.json', state)
        return receipt


def loopback(case_id, proposal_ref, root=ROOT):
    case = case_path(case_id, root)
    with locked(case):
        state = load(case / 'state.json')
        state_sha = digest(case / 'state.json')
        proposal = load(local(case, proposal_ref))
        schema_check(proposal, 'loopback', root)
        if proposal['case_id'] != case_id or proposal['state_sha256'] != state_sha:
            raise ValueError('Loopback state/identity mismatch')
        for proof in proposal['evidence']:
            if digest(local(case, proof['ref'])) != proof['sha256']:
                raise ValueError('Loopback evidence changed')
        for adr in proposal['adr_refs']:
            local(root, adr)
        if proposal['action'] == 'experiment' and not proposal['experiment']:
            raise ValueError('Experiment action requires protocol')
        metrics = proposal['metrics']
        for m in metrics:
            if m['status'] == 'observed' and (m['before'] is None or m['after'] is None or not m['evidence_refs']):
                raise ValueError('Observed metric requires before/after and proof')
            if m['status'] != 'observed' and (m['before'] is not None or m['after'] is not None):
                raise ValueError('Unknown metric cannot invent values')
            if not set(m['evidence_refs']) <= {e['ref'] for e in proposal['evidence']}:
                raise ValueError('Metric references unresolved evidence')
            if m['status'] == 'observed':
                for side in ('before', 'after'):
                    reading = m.get(side + '_reading')
                    if not reading or reading['ref'] not in m['evidence_refs']:
                        raise ValueError('Observed measurement requires pinned JSON reading')
                    actual = pointer(load(local(case, reading['ref'])), reading['pointer'])
                    if isinstance(actual, bool) or not isinstance(actual, (int, float)) or actual != m[side]:
                        raise ValueError('Observed metric differs from recorded measurement')
        guide = process(root)['loopback_axes'][proposal['axis']]
        return {'status': 'proposal_validated_not_applied', 'case_id': case_id,
                'proposal_sha256': digest(local(case, proposal_ref)), 'state_sha256': state_sha,
                'stale_refs': verify(state, case, root, allow_stale=True),
                'investigation': guide, 'github_writes': False, 'run_mutated': False,
                'semantic_cause_verified': False, 'business_approval': False}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command', choices=['check', 'init', 'begin', 'complete', 'status', 'invalidate', 'loopback', 'render'])
    parser.add_argument('--case')
    parser.add_argument('--root', type=Path, default=ROOT)
    parser.add_argument('--input', type=Path)
    parser.add_argument('--stage')
    parser.add_argument('--actor', default='manual_agent')
    parser.add_argument('--reason', default='')
    parser.add_argument('--proposal')
    args = parser.parse_args(argv)
    try:
        if args.command == 'check': result = check_contracts(args.root)
        elif args.command == 'init': result = init(args.case, load(args.input), args.root)
        elif args.command == 'begin': result = begin(args.case, args.stage, args.actor, args.root)
        elif args.command == 'complete': result = complete(args.case, args.stage, args.root)
        elif args.command == 'invalidate': result = invalidate(args.case, args.stage, args.reason, args.root)
        elif args.command == 'loopback': result = loopback(args.case, args.proposal, args.root)
        elif args.command == 'render': result = render(args.case, args.root)
        else: result = inspect(args.case, args.root)
        print(json.dumps(result, ensure_ascii=False, indent=2))
    except Exception as exc:
        print(json.dumps({'status': 'blocked', 'error': str(exc)}))
        return 1
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
