"""Append the fourth actual C decision; never modify previous artifacts."""
import hashlib
import json
import os
import re
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
HERE = Path(__file__).resolve().parent
PREV = P / 'evaluation/M-POC1C-review-004'
C = P / 'evaluation/eval-v1-candidate-20261008-02'
ALLOWED = ['docs/STATUS.md', 'docs/ROADMAP.md', 'docs/HANDOFF.md']
HANDOFF = 'docs/handoff/2026-10-09-M-POC1C-review-005.md'

def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))

def ref(path):
    with path.open('rb') as stream:
        digest = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': digest, 'bytes': path.stat().st_size}

def save(name, value):
    with (HERE / name).open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')

def git(*args):
    return subprocess.run(['git', '-c', 'safe.directory=C:/dev/wargame-compiler', *args], cwd=ROOT,
                          env={**os.environ, 'GIT_OPTIONAL_LOCKS': '0'}, capture_output=True,
                          text=True, check=True).stdout.strip()

now = datetime.now(timezone.utc).isoformat()
assert git('branch', '--show-current') == 'feature/tests'
git('merge-base', '--is-ancestor', '90535261a4498cabcd6abc0af33b56a4267b6193', 'HEAD')
head = git('rev-parse', 'HEAD')
assert not (P / 'evaluation/eval-v1').exists()
assert not (P / 'evaluation/freeze-public-v1.json').exists()
candidate = load(C / 'manifest.json')
for item in [*candidate['artifacts'], *candidate['provenance']]:
    assert ref(ROOT / item['path']) == item, item

if sys.argv[1] == 'record':
    seal = load(PREV / 'closure-seal-after-decision-03.json')
    for item in [seal['review_manifest'], seal['completion'], seal['measurement_completion'], *seal['public_documents']]:
        assert ref(ROOT / item['path']) == item, item
    paths = {ROOT / item['path'] for item in load(PREV / 'baseline.json')['files']}
    paths.update(path for path in PREV.iterdir() if path.is_file())
    paths.update(path for path in C.iterdir() if path.is_file())
    paths.add(ROOT / 'docs/handoff/2026-10-09-M-POC1C-review-004.md')
    save('baseline.json', {'recorded_at_utc': now, 'files': [ref(path) for path in sorted(paths)], 'allowed_public_updates': ALLOWED})
    question = load(PREV / 'pending-question-04-DEP024.json')
    assert (HERE / 'owner-answer-04.raw.txt').read_text(encoding='utf-8').rstrip('\n') == 'zatwierdzam'
    decision = {
        'id': 'M-POC1C-owner-decision-04', 'card': 'M-POC1C', 'question_id': question['id'],
        'date': '2026-10-09', 'date_source': 'client time context', 'timezone': 'Europe/Warsaw',
        'recorded_at_utc': now, 'user_message_timestamp': 'unknown',
        'reviewer': 'owner in this chat; no personal identity attributed',
        'actual_owner_response': 'zatwierdzam', 'raw_response': ref(HERE / 'owner-answer-04.raw.txt'),
        'capture_method': 'Verbatim user message copied from this conversation with a terminal LF.',
        'approved_question': 'Czy zatwierdzasz to powiązanie?',
        'shown_proposal': '9.82 odsyła do zasad Active Fire w 9.85 — maksymalnie dwa strzały na turę, najwyżej jeden na przyjazną fazę rozkazów, we wskazanym segmencie. Brak wymogu rozkazu nie znosi ograniczeń 9.82: Scorpio musi być w trybie Fire i nie może strzelać w fazie, w której właśnie przełączono go na Fire.',
        'shown_source_excerpt': question['shown_source_excerpt'],
        'approved_scope': {**question['proposed_tuple'], 'necessity_scope': question['plain_language_proposal'],
                           'target_scope': question['scope_limits'], 'retain_all_target_conditions': True},
        'criticality': 'critical in previously approved local mode/schedule scope',
        'criticality_basis': question['criticality_basis'], 'new_separate_criticality_statement_by_owner': False,
        'basis': [ref(PREV / 'pending-question-04-DEP024.json'), ref(C / 'manifest.json'), ref(P / 'evaluation/draft/dependencies.json')],
        'not_approved': ['Other proposed relation tuples', 'Actual CRT/geometry/full game outcomes', 'Whole target record or metadata',
                         'Scoring grouping/rubrics', 'eval-v1 freeze', 'M-POC2A/B'],
        'new_situations': [], 'freeze_authorized': False, 'frozen': False,
    }
    save('decision-04-DEP024.json', decision)
    counts = {'confirmed_explicit_execution': 4, 'confirmed_implicit_execution': 3,
              'unconfirmed_explicit_execution': 95, 'unconfirmed_implicit_execution': 11,
              'mentions_separate': 7, 'continuations_separate': 7, 'parent_facets': 127}
    save('dependency-overlay-04.json', {
        'id': 'M-POC1C-dependency-overlay-04', 'authorizing_decision': ref(HERE / 'decision-04-DEP024.json'),
        'base_candidate_manifest': ref(C / 'manifest.json'), 'previous_overlay': ref(PREV / 'dependency-overlay-03.json'),
        'operation': 'add DEP-024 in confirmed set and remove it from unconfirmed set during materialization',
        'confirmed_relation': {**decision['approved_scope'], 'executable': True, 'target_status': 'internal',
                              'review_status': 'owner_confirmed_exact_scope', 'criticality': decision['criticality'],
                              'criticality_basis': decision['criticality_basis'], 'source_evidence': question['source_evidence'],
                              'target_evidence': question['target_evidence'], 'owner_decision': ref(HERE / 'decision-04-DEP024.json')},
        'counts_after_overlay': counts, 'original_artifacts_modified': [], 'freeze_authorized': False,
    })
    save('change-map-decision-04.json', {
        'decision': ref(HERE / 'decision-04-DEP024.json'), 'overlay': ref(HERE / 'dependency-overlay-04.json'),
        'parent': ref(C / 'manifest.json'), 'id': 'DEP-024', 'from': 'unconfirmed_relation_fields',
        'to': 'owner_confirmed_explicit_local_procedure_use',
        'counts_delta': {'confirmed_explicit_execution': 1, 'unconfirmed_explicit_execution': -1}, 'original_artifacts_modified': [],
    })
    dep = next(row for row in load(P / 'evaluation/draft/dependencies.json')['dependencies'] if row['id'] == 'DEP-041')
    target = next(row for row in load(P / 'evaluation/draft/inventory.json')['items'] if row['id'] == 'T-01')
    save('pending-question-05-DEP041.json', {
        'id': 'M-POC1C-RQ-05-DEP041', 'status': 'waiting_owner_decision',
        'source_evidence': dep['evidence'][0], 'target_evidence': target['evidence'][0],
        'shown_source_excerpt': 'Each time an Elephant unit routs, its player rolls the die and does one of the following, depending on the DR:',
        'plain_language_proposal': 'The die procedure in 9.14 uses the local Die Roll/Result table T-01 on PDF32, spanning left rows 0 and 1–6 and right row 7–9. Retain the first/subsequent Rampage DR distinction and existing approved Leader Elephant exceptions, without guessing actual compass/map directions or equating the 4.84 trigger die with this first directional die.',
        'proposed_tuple': {key: dep[key] for key in ('id', 'from', 'to', 'kind', 'explicitness')},
        'criticality_basis': ref(P / 'evaluation/owner-review-002/decision-18-RQ-15c1.json'),
        'scope_limits': 'Internal table identity/use only, respecting separately approved row scopes and limitations. No whole-table metadata/glyph certificate, actual map/nearest-unit/compass, general Rout or 4.84-to-9.14 roll sequencing approval.',
        'target_evidence_all': target['evidence'],
        'source_span_identity': 'Local unnumbered Die Roll/Result table under 9.14; T-01 is a local reference, not a printed publisher table number.',
        'actual_owner_answer': None, 'freeze_authorization_requested': False,
    })
    previous = load(PREV / 'review-state-after-decision-03.json')
    save('review-state-after-decision-04.json', {
        'recorded_at_utc': now, 'date': '2026-10-09', 'card': 'M-POC1C', 'result': 'partial', 'workflow_status': 'waiting_review',
        'base_candidate': ref(C / 'manifest.json'),
        'overlays_in_order': [*previous['overlays_in_order'], ref(HERE / 'dependency-overlay-04.json')],
        'actual_owner_decisions': 4, 'counts': counts,
        'confirmed_execution_ids': [*previous['confirmed_execution_ids'], 'DEP-024'],
        'situations': previous['situations'], 'remaining_internal_explicit_tuple_questions': ['DEP-041'],
        'remaining_freeze_gates': previous['remaining_freeze_gates'], 'next_question': 'M-POC1C-RQ-05-DEP041',
        'milestone': 'M-POC1', 'milestone_status': 'next', 'next_card': 'M-POC1C', 'freeze_authorized': False, 'frozen': False,
    })
    print(json.dumps({'decision': ref(HERE / 'decision-04-DEP024.json'), 'counts': counts}, indent=2))
elif sys.argv[1] == 'close':
    check_root = (ROOT / sys.argv[2]).resolve()
    assert check_root.is_relative_to((ROOT / 'private/poc/_checks').resolve())
    result = load(check_root / 'result.json')
    assert result['tests_exit'] == result['diff_exit'] == 0
    pytest_log = (check_root / 'pytest.log').read_text(encoding='utf-8-sig')
    assert re.search(r'\b91 passed\b', pytest_log), pytest_log
    baseline = load(HERE / 'baseline.json')
    preserved, changed = [], []
    for item in baseline['files']:
        actual = ref(ROOT / item['path'])
        if item != actual:
            assert item['path'] in ALLOWED, (item, actual)
            changed.append({'before': item, 'after': actual})
        else:
            preserved.append(actual)
    state = load(HERE / 'review-state-after-decision-04.json')
    relations = list(load(C / 'dependencies.json')['confirmed_execution_relations'])
    for item in state['overlays_in_order']:
        assert ref(ROOT / item['path']) == item
        overlay = load(ROOT / item['path'])
        assert ref(ROOT / overlay['authorizing_decision']['path']) == overlay['authorizing_decision']
        relations.append(overlay['confirmed_relation'])
    assert len({(r['from'], r['to'], r['kind'], r['explicitness']) for r in relations}) == 7
    assert sum(r['explicitness'] == 'explicit' for r in relations) == 4
    assert sum(state['counts'][key] for key in state['counts'] if key != 'parent_facets') == 127
    git('diff', '--check')
    save('review-manifest-after-decision-04.json', {
        'recorded_at_utc': now, 'card': 'M-POC1C', 'status': 'partial/waiting_review',
        'files': [ref(path) for path in sorted(HERE.iterdir()) if path.is_file()], 'base_candidate': ref(C / 'manifest.json'),
        'previous_closure': ref(PREV / 'closure-seal-after-decision-03.json'), 'counts': state['counts'], 'frozen': False,
    })
    completion = {
        'id': 'M-POC1C-review-005-after-decision-04', 'recorded_at_utc': now, 'date': '2026-10-09', 'timezone': 'Europe/Warsaw',
        'card': 'M-POC1C', 'outcome': 'partial', 'workflow_status': 'waiting_review', 'milestone': 'M-POC1',
        'milestone_status': 'next', 'next_card': 'M-POC1C', 'branch': 'feature/tests', 'head': head,
        'decision': ref(HERE / 'decision-04-DEP024.json'), 'review_manifest': ref(HERE / 'review-manifest-after-decision-04.json'),
        'candidate_and_overlays': {'candidate': ref(C / 'manifest.json'), 'overlays_in_order': state['overlays_in_order']},
        'counts': state['counts'], 'situations': state['situations'], 'pending_question': ref(HERE / 'pending-question-05-DEP041.json'),
        'checks': {'scripts_check': '91 passed', 'result': result, 'local_TMP_TEMP': str(check_root / 'temp'),
                   'new_basetemp': True, 'logs': [ref(check_root / 'pytest.log'), ref(check_root / 'result.json')], 'final_git_diff_check_exit': 0},
        'preservation': {'baseline_checked': len(baseline['files']), 'unchanged': len(preserved),
                         'preserved_files': preserved, 'intentional_public_updates': changed},
        'measurement': {'model_selector_owner_report': 'sol', 'exact_model_version': 'unknown', 'reasoning_selector': 'unknown',
                        'active_work_time': 'unknown', 'user_active_time': 'unknown', 'tokens': 'unknown', 'cost': 'unknown', 'calendar_time_is_active_work': False},
        'remaining_gates': state['remaining_freeze_gates'], 'freeze_authorized': False, 'frozen': False,
        'semantic_extraction_run': False, 'plan_thresholds_changed': False, 'plan_limits_changed': False, 'forbidden_work_performed': [],
    }
    save('completion-after-decision-04.json', completion)
    measurement = P / 'measurement/M-POC1C-review-005'
    measurement.mkdir()
    with (measurement / 'completion.json').open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(completion, ensure_ascii=False, indent=2) + '\n')
    save('closure-seal-after-decision-04.json', {
        'recorded_at_utc': now, 'card': 'M-POC1C', 'outcome': 'partial', 'workflow_status': 'waiting_review', 'frozen': False,
        'review_manifest': ref(HERE / 'review-manifest-after-decision-04.json'), 'completion': ref(HERE / 'completion-after-decision-04.json'),
        'measurement_completion': ref(measurement / 'completion.json'), 'public_documents': [ref(ROOT / name) for name in (*ALLOWED, HANDOFF)],
        'next_question': state['next_question'], 'counts': state['counts'], 'no_self_hash_cycle': True,
    })
    print(json.dumps({'seal': ref(HERE / 'closure-seal-after-decision-04.json'), 'preserved_files': len(preserved), 'checks': '91 passed'}, indent=2))
else:
    raise SystemExit('Use record or close CHECK_ROOT.')
