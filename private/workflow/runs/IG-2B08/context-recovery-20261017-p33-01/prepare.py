"""Authorize fresh B08 execution after a bounded page-33 context incident."""
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[5]
sys.path.insert(0, str(ROOT / 'scripts'))
import orchestrate_ig2 as o
import workflow as w

PREP = 'private/workflow/runs/IG-2B08/context-recovery-20261017-p33-01/'
OLD = 'private/workflow/runs/IG-2B08/inventory-8d84cd90-01/'
NEW = 'private/workflow/runs/IG-2B08/inventory-p33-scope02/'
ACTOR = 'coordinator:operator-page33-scope-recovery-20261017-01'
CONFIG = 'Exact coordinating model/reasoning metadata unavailable. This is not an executor claim; fresh observed gpt-6.1-sol/high is required for execution/review.'


def pin(rel):
    p = w.safe_path(ROOT, rel)
    return {'path': rel, 'sha256': w.digest(p), 'bytes': p.stat().st_size}


def write(name, value):
    p = ROOT / PREP / name
    with p.open('x', encoding='utf-8', newline='\n') as f:
        json.dump(value, f, ensure_ascii=False, indent=2)
        f.write('\n')
    return pin(PREP + name)


def stamp(summary):
    return {'role': 'coordinator', 'actor': ACTOR, 'model': None, 'reasoning': None,
            'configuration_evidence': CONFIG, 'summary': summary}


def canonical_hash(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def main():
    q = w.read_json(ROOT / w.QUEUE)
    w.validate(q, ROOT)
    before = w.digest(ROOT / w.QUEUE)
    task = next(t for t in q['tasks'] if t['id'] == 'IG-2B08')
    original = copy.deepcopy(task)
    if task['status'] != 'blocked' or task['events'][-1]['evidence'] != OLD + 'blocked.json':
        raise ValueError('Selected incident/status changed')
    if (ROOT / NEW).exists() or (ROOT / 'private/workflow/ig2-orchestrator.lock').exists() or (ROOT / 'private/workflow/queue.lock').exists():
        raise ValueError('Ownership is not available')
    triage = w.read_json(ROOT / PREP / 'process-triage.json')
    when = datetime.fromisoformat(triage['observed_utc'].replace('Z', '+00:00'))
    if triage['processes'] or (datetime.now(timezone.utc) - when).total_seconds() > 600:
        raise ValueError('Refresh previous-owner liveness evidence')
    incident = pin(OLD + 'source-context-incident.json')
    blocked = pin(OLD + 'blocked.json')
    if blocked['sha256'] != task['events'][-1]['sha256']:
        raise ValueError('Blocked evidence changed')
    o.verify_artifacts(ROOT, w.read_json(ROOT / blocked['path']))
    checkpoint = w.read_json(ROOT / (OLD + 'checkpoint-blocked.json'))
    o.verify_artifacts(ROOT, {'artifacts': checkpoint['base_files'] + checkpoint['changed_files']})
    files = [pin(p.relative_to(ROOT).as_posix()) for p in sorted((ROOT / OLD).rglob('*'))
             if p.is_file() and '__pycache__' not in p.parts]
    preserved = write('preserve-manifest.json', {'format': 'wgc-incident-attempt-preservation-1',
        'attempt': OLD, 'artifacts': files, 'unaccepted': True,
        'scope': 'Byte preservation only. No old renderer, source image, extracted text or inspection/check claim is authorized fresh executor context.'})
    source = pin('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf')
    if source['sha256'] != 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e':
        raise ValueError('Official source changed')
    proof = pin(PREP + 'context-boundary-verification.json')
    o.verify_artifacts(ROOT, w.read_json(ROOT / proof['path']))
    original_input = copy.deepcopy(task['inventory_contract']['input_pins'])
    if w.digest(ROOT / original_input['path']) != original_input['sha256']:
        raise ValueError('Original input contract changed')
    inputs = w.read_json(ROOT / original_input['path'])
    inputs = {k: v for k, v in inputs.items() if k not in ('model', 'reasoning', 'configuration_evidence', 'configuration_sha256', 'actor', 'role')}
    inputs.update(stamp('Fresh operational context contract: exact page-33 continuation bounds, original accepted dependency/input pins unchanged.'))
    inputs['original_contract'] = original_input
    inputs['executor_attempt_root'] = NEW.rstrip('/')
    inputs['product_outputs'] = [p.replace(OLD, NEW) for p in inputs['product_outputs']]
    inputs['source_access']['context_only'] = [
        {'physical_page': 28, 'scope': 'Reference-only: use the accepted direct dependency exit observation through the prepared dependency projection and preserve baseline continuation records. Do not render/extract page 28 again in this session; assigned page 29 is freshly inspected. If additional original-page context is indispensable, stop for a new bounded contract.'},
        {'physical_page': 33, 'scope': 'Only the initial two continuation lines from page 32, before the following note. No subsequent note, heading, rule or right column.',
         'frame': 'unrotated effective crop top-left, PDF points; source page 612 x 792, rotation 0, UserUnit 1',
         'box_points': [45, 50, 306, 80],
         'box_normalized': [73529, 63131, 500000, 101011],
         'rounding': 'The normalized box is explicitly authorized as the outward million-unit rounding of the point box; its sub-millipoint margin contains no additional content.',
         'raster_144dpi': {'x': 90, 'y': 100, 'width': 522, 'height': 60},
         'access_protocol': 'Set crop bounds before text extraction or releasing pixels. Use original-page clipping before extract_text, and native raster crop parameters before rendering output. Never inspect a full page-33 render or extract raw text from a crop PDF whose page streams may retain out-of-box content. No automatic box expansion.'}]
    effective = write('input-pins.json', inputs)
    assessment = write('assessment.json', dict(stamp('The incident arose from an estimated lower crop bound in an underspecified verbal context scope; a fresh executor with an exact rectangle resolves access scope without accepting prior results.'),
        operator_request_verbatim='Oceń incydent z wycinkiem strony 33, popraw zakres kontekstu i wznów orkiestrator od IG-2B08 w świeżej sesji.',
        incident=incident, blocked=blocked, preservation=preserved,
        prior_actual_box_points=[45, 50, 298, 127], corrected_box_points=[45, 50, 306, 80],
        correction_basis={'continuation_line_bottom': 76.0036, 'following_note_first_glyph_top': 84.507,
                          'continuation_max_right': 299.548, 'complete_continuation_lines': 2,
                          'proof': proof, 'visual_review': 'The fresh bounded PNG contains both complete continuation lines and no following note.'},
        diagnostic_limit='The first geometry-only probe of the old crop PDF showed retained out-of-clip page-stream geometry; no source text was emitted. Authoritative geometry was recomputed on the original page with explicit cropping before characters/text were released. Old crop PDFs are not safe generic text-extraction inputs.',
        required_recovery='A new absent attempt and ephemeral observed Sol/high session; freshly inspect all assigned original pages and the exact page-33 continuation rectangle, author inventory, derive serial evidence and two complete replays, run all unchanged checks and obtain independent review.',
        no_prior_inspection_or_tests_inherited=True, no_source_or_semantic_acceptance_granted=True))
    scope = write('scope.json', {
        **stamp('Operator-authorized fresh B08 execution scope after source-context incident assessment.'),
        'format': 'wgc-source-context-recovery-1', 'task': task['id'],
        'mode': 'fresh_rebuild_no_drafts', 'incident': incident, 'blocked_evidence': blocked,
        'preserved_attempt': OLD, 'preserve_manifest': preserved, 'fresh_attempt': NEW,
        'effective_input_contract': effective, 'assessment': assessment,
        'assigned_physical_pages': [29, 30, 31, 32],
        'fresh_original_context': [inputs['source_access']['context_only'][1]],
        'incoming_context_policy': inputs['source_access']['context_only'][0],
        'acceptance_sha256': canonical_hash(original['acceptance']),
        'original_tests_sha256': canonical_hash(original['tests']),
        'command_path_mapping': {'from': OLD, 'to': NEW, 'purpose': 'Replace only frozen prior-attempt output/test operands; never alter test assertions or suites.'},
        'reuse_policy': 'No prior draft, image, extracted text, derivation helper, transcript, inspection or check result is an execution input. Accepted dependency/source pins remain authoritative. Boundary proof gives coordinates only; fresh inspection/evidence must be regenerated.',
        'preservation_checks': 'Internally hash every artifact named by preserve-manifest.json before product writes and again before delivery; print only verification counts/status, never manifest contents or old source text. Independent review verifies preservation again.',
        'stop_policy': 'Any extra context requirement, clipped continuation or helper refusal ends this session for fresh coordinator refinement. Do not estimate a larger rectangle or silently include the following note.',
        'human_semantic_acceptance': False, 'gameplay_readiness': False})
    authorization = write('authorization.json', dict(stamp('The current human explicitly authorized incident assessment, precise context correction and a fresh IG-2B08 session.'),
        operator_requested_recovery=True, criteria=task['acceptance'], artifacts=[scope, assessment, effective, preserved, incident]))
    task['outputs'] = [p.replace(OLD, NEW) for p in task['outputs']]
    task['write_scope'] = [NEW]
    task['start_conditions'] = [s.replace(OLD.rstrip('/'), NEW.rstrip('/')) for s in task['start_conditions']]
    task['start_conditions'] += [
        'FIRST read the new context recovery scope and assessment, then the effective input contract. The old attempt is immutable and grants no inherited inspection, tests, delivery or acceptance.',
        'Fresh source access is exactly pages 29-32 plus the pinned page-33 continuation rectangle. Page 28 is reference-only through the direct accepted dependency projection; no original-page access there in this session. No full-page page-33 output or automatic crop expansion.']
    task['tests'] += [
        'Operational recovery binding: original commands above remain required with only the prior attempt prefix inventory-8d84cd90-01 replaced by inventory-p33-scope02. Do not run test basetemp or write any artifact into the frozen attempt. Preserve every original suite/assertion and verify the new context boundary before access.',
        'Verify all old-attempt artifact hashes using the pinned preservation manifest before product writes and at delivery; verify page-33 context pixels/text exclude the following note and use exact source/page/box pins.']
    task['inputs'] = [s.replace(original_input['path'], effective['path']) for s in task['inputs']]
    task['context'] = [effective['path'] if p == original_input['path'] else p for p in task['context']]
    task['context'] += [scope['path'], assessment['path']]
    task['inventory_contract']['input_pins'] = effective
    task['inventory_contract']['attempt_root'] = NEW.rstrip('/')
    task['inventory_contract']['fresh_context_only_physical_pages'] = [33]
    task['inventory_contract']['source_access'] = inputs['source_access']
    task['context_recovery_authorization'] = {'incident': incident, 'scope': scope, 'assessment': assessment}
    policy = w.read_json(ROOT / 'docs/work/context-policy.json')
    for rel in (effective['path'], scope['path'], assessment['path']):
        if rel not in policy['allow']:
            policy['allow'].append(rel)
    o.dump(ROOT / 'docs/work/context-policy.json', policy)
    if task['acceptance'] != original['acceptance'] or task['tests'][:len(original['tests'])] != original['tests']:
        raise ValueError('Original criteria/tests changed')
    if w.digest(ROOT / w.QUEUE) != before:
        raise ValueError('Queue changed during recovery preparation')
    w.validate(q, ROOT, check_views=False)
    o.dump(ROOT / w.QUEUE, q)
    w.render(q, ROOT)
    write('task-before.json', original)
    write('task-after.json', task)
    for state, summary in (
        ('planned', 'Incident assessed; explicit current human recovery authorization and exact context bounds resolve the blocker.'),
        ('ready', 'Accepted input hashes, exact context bounds, fresh absent ownership and original criteria/tests are pinned; ready for a fresh observed Sol/high executor.')):
        evidence = write(state + '.json', dict(stamp(summary), criteria=task['acceptance'], artifacts=[scope, assessment, effective, authorization, preserved, incident]))
        subprocess.run([sys.executable, 'scripts/workflow.py', 'transition', '--task', task['id'],
                        '--to', state, '--evidence', evidence['path']], cwd=ROOT, check=True)
    o.verify_artifacts(ROOT, {'artifacts': files})
    write('preparation-result.json', {'task': task['id'], 'status': 'ready',
        'fresh_attempt': NEW, 'preserved_artifacts': len(files), 'queue_sha256': w.digest(ROOT / w.QUEUE)})
    print(json.dumps({'task': task['id'], 'ready': True, 'preserved_artifacts': len(files), 'fresh_attempt': NEW}))


if __name__ == '__main__':
    main()
