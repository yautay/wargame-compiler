"""Append the fifth actual C decision; never modify previous artifacts."""
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
PREV = P / 'evaluation/M-POC1C-review-005'
C = P / 'evaluation/eval-v1-candidate-20261008-02'
ALLOWED = ['docs/STATUS.md', 'docs/ROADMAP.md', 'docs/HANDOFF.md']
HANDOFF = 'docs/handoff/2026-10-09-M-POC1C-review-006.md'

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
    seal = load(PREV / 'closure-seal-after-decision-04.json')
    for item in [seal['review_manifest'], seal['completion'], seal['measurement_completion'], *seal['public_documents']]:
        assert ref(ROOT / item['path']) == item, item
    paths = {ROOT / item['path'] for item in load(PREV / 'baseline.json')['files']}
    paths.update(path for path in PREV.iterdir() if path.is_file())
    paths.update(path for path in C.iterdir() if path.is_file())
    paths.add(ROOT / 'docs/handoff/2026-10-09-M-POC1C-review-005.md')
    save('baseline.json', {'recorded_at_utc': now, 'files': [ref(path) for path in sorted(paths)], 'allowed_public_updates': ALLOWED})
    question = load(PREV / 'pending-question-05-DEP041.json')
    assert (HERE / 'owner-answer-05.raw.txt').read_text(encoding='utf-8').rstrip('\n') == 'zatwierdzam'
    decision = {
        'id': 'M-POC1C-owner-decision-05', 'card': 'M-POC1C', 'question_id': question['id'],
        'date': '2026-10-09', 'date_source': 'client time context', 'timezone': 'Europe/Warsaw',
        'recorded_at_utc': now, 'user_message_timestamp': 'unknown',
        'reviewer': 'owner in this chat; no personal identity attributed',
        'actual_owner_response': 'zatwierdzam', 'raw_response': ref(HERE / 'owner-answer-05.raw.txt'),
        'capture_method': 'Verbatim user message copied from this conversation with a terminal LF.',
        'approved_question': 'Czy zatwierdzasz powiązanie 9.14 → ta lokalna tabela?',
        'shown_proposal': '9.14 korzysta z lokalnej tabeli Die Roll / Result — wiersze 0 i 1–6 są w lewej kolumnie, a 7–9 w prawej. Zachowujemy już uzgodnione rozróżnienie pierwszego i kolejnych rzutów Rampage oraz wyjątki dla Leader Elephant. Nie zatwierdzamy przy tym rzeczywistych kierunków na mapie ani utożsamienia rzutu wyzwalającego z 4.84 z pierwszym rzutem kierunkowym 9.14.',
        'shown_source_excerpt': question['shown_source_excerpt'],
        'approved_scope': {**question['proposed_tuple'], 'necessity_scope': question['plain_language_proposal'],
                           'target_scope': question['scope_limits'], 'retain_all_target_conditions': True,
                           'local_target_identity': question['source_span_identity']},
        'criticality': 'critical in previously approved local Rampage-table scope',
        'criticality_basis': question['criticality_basis'], 'new_separate_criticality_statement_by_owner': False,
        'basis': [ref(PREV / 'pending-question-05-DEP041.json'), ref(C / 'manifest.json'), ref(P / 'evaluation/draft/dependencies.json')],
        'not_approved': ['Other proposed relation tuples', 'Actual CRT/geometry/full game outcomes', 'Whole target record or metadata',
                         'Scoring grouping/rubrics', 'eval-v1 freeze', 'M-POC2A/B'],
        'new_situations': [], 'freeze_authorized': False, 'frozen': False,
    }
    save('decision-05-DEP041.json', decision)
    counts = {'confirmed_explicit_execution': 5, 'confirmed_implicit_execution': 3,
              'unconfirmed_explicit_execution': 94, 'unconfirmed_implicit_execution': 11,
              'mentions_separate': 7, 'continuations_separate': 7, 'parent_facets': 127}
    save('dependency-overlay-05.json', {
        'id': 'M-POC1C-dependency-overlay-05', 'authorizing_decision': ref(HERE / 'decision-05-DEP041.json'),
        'base_candidate_manifest': ref(C / 'manifest.json'), 'previous_overlay': ref(PREV / 'dependency-overlay-04.json'),
        'operation': 'add DEP-041 in confirmed set and remove it from unconfirmed set during materialization',
        'confirmed_relation': {**decision['approved_scope'], 'executable': True, 'target_status': 'internal',
                              'review_status': 'owner_confirmed_exact_scope', 'criticality': decision['criticality'],
                              'criticality_basis': decision['criticality_basis'], 'source_evidence': question['source_evidence'],
                              'target_evidence': question['target_evidence'], 'target_evidence_all': question['target_evidence_all'], 'owner_decision': ref(HERE / 'decision-05-DEP041.json')},
        'counts_after_overlay': counts, 'original_artifacts_modified': [], 'freeze_authorized': False,
    })
    save('change-map-decision-05.json', {
        'decision': ref(HERE / 'decision-05-DEP041.json'), 'overlay': ref(HERE / 'dependency-overlay-05.json'),
        'parent': ref(C / 'manifest.json'), 'id': 'DEP-041', 'from': 'unconfirmed_relation_fields',
        'to': 'owner_confirmed_explicit_local_table_use',
        'counts_delta': {'confirmed_explicit_execution': 1, 'unconfirmed_explicit_execution': -1}, 'original_artifacts_modified': [],
    })
    previous = load(PREV / 'review-state-after-decision-04.json')
    save('review-state-after-decision-05.json', {
        'recorded_at_utc': now, 'date': '2026-10-09', 'card': 'M-POC1C', 'result': 'partial', 'workflow_status': 'waiting_review',
        'base_candidate': ref(C / 'manifest.json'),
        'overlays_in_order': [*previous['overlays_in_order'], ref(HERE / 'dependency-overlay-05.json')],
        'actual_owner_decisions': 5, 'counts': counts,
        'confirmed_execution_ids': [*previous['confirmed_execution_ids'], 'DEP-041'],
        'situations': previous['situations'], 'remaining_internal_explicit_tuple_questions': [],
        'remaining_freeze_gates': ['Scoring grouping/category rubrics and retained limitations', 'Distinct actual owner freeze decision'], 'next_question': 'M-POC1C-RQ-06-scope',
        'milestone': 'M-POC1', 'milestone_status': 'next', 'next_card': 'M-POC1C', 'freeze_authorized': False, 'frozen': False,
    })
    print(json.dumps({'decision': ref(HERE / 'decision-05-DEP041.json'), 'counts': counts}, indent=2))
elif sys.argv[1] == 'close':
    check_root = (ROOT / sys.argv[2]).resolve()
    assert check_root.is_relative_to((ROOT / 'private/poc/_checks').resolve())
    result = load(check_root / 'result.json')
    assert result['tests_exit'] == result['diff_exit'] == 0
    pytest_log = (check_root / 'pytest.log').read_text(encoding='utf-8-sig')
    assert re.search(r'\b92 passed\b', pytest_log), pytest_log
    baseline = load(HERE / 'baseline.json')
    preserved, changed = [], []
    for item in baseline['files']:
        actual = ref(ROOT / item['path'])
        if item != actual:
            assert item['path'] in ALLOWED, (item, actual)
            changed.append({'before': item, 'after': actual})
        else:
            preserved.append(actual)
    state = load(HERE / 'review-state-after-decision-05.json')
    relations = list(load(C / 'dependencies.json')['confirmed_execution_relations'])
    for item in state['overlays_in_order']:
        assert ref(ROOT / item['path']) == item
        overlay = load(ROOT / item['path'])
        assert ref(ROOT / overlay['authorizing_decision']['path']) == overlay['authorizing_decision']
        relations.append(overlay['confirmed_relation'])
    assert len({(r['from'], r['to'], r['kind'], r['explicitness']) for r in relations}) == 8
    assert sum(r['explicitness'] == 'explicit' for r in relations) == 5
    assert sum(state['counts'][key] for key in state['counts'] if key != 'parent_facets') == 127
    materialized = P / 'evaluation/eval-v1-candidate-20261009-03/manifest.json'
    validation = load(HERE / 'candidate-validation.json')
    assert ref(materialized) == validation['candidate_manifest']
    for item in [*load(materialized)['artifacts'], *load(materialized)['provenance']]:
        assert ref(ROOT / item['path']) == item, item
    git('diff', '--check')
    save('review-manifest-after-decision-05.json', {
        'recorded_at_utc': now, 'card': 'M-POC1C', 'status': 'partial/waiting_review',
        'files': [ref(path) for path in sorted(HERE.iterdir()) if path.is_file()], 'base_candidate': ref(C / 'manifest.json'), 'materialized_candidate': ref(P / 'evaluation/eval-v1-candidate-20261009-03/manifest.json'),
        'previous_closure': ref(PREV / 'closure-seal-after-decision-04.json'), 'counts': state['counts'], 'frozen': False,
    })
    completion = {
        'id': 'M-POC1C-review-006-after-decision-05', 'recorded_at_utc': now, 'date': '2026-10-09', 'timezone': 'Europe/Warsaw',
        'card': 'M-POC1C', 'outcome': 'partial', 'workflow_status': 'waiting_review', 'milestone': 'M-POC1',
        'milestone_status': 'next', 'next_card': 'M-POC1C', 'branch': 'feature/tests', 'head': head,
        'decision': ref(HERE / 'decision-05-DEP041.json'), 'review_manifest': ref(HERE / 'review-manifest-after-decision-05.json'),
        'candidate_and_overlays': {'candidate': ref(C / 'manifest.json'), 'overlays_in_order': state['overlays_in_order'], 'materialized_candidate': ref(P / 'evaluation/eval-v1-candidate-20261009-03/manifest.json')},
        'counts': state['counts'], 'situations': state['situations'], 'pending_question': ref(HERE / 'pending-question-06-scope.json'),
        'checks': {'scripts_check': '92 passed', 'result': result, 'local_TMP_TEMP': str(check_root / 'temp'),
                   'new_basetemp': True, 'logs': [ref(check_root / 'pytest.log'), ref(check_root / 'result.json')], 'final_git_diff_check_exit': 0},
        'preservation': {'baseline_checked': len(baseline['files']), 'unchanged': len(preserved),
                         'preserved_files': preserved, 'intentional_public_updates': changed},
        'measurement': {'model_selector_owner_report': 'sol', 'exact_model_version': 'unknown', 'reasoning_selector': 'unknown',
                        'active_work_time': 'unknown', 'user_active_time': 'unknown', 'tokens': 'unknown', 'cost': 'unknown', 'calendar_time_is_active_work': False},
        'remaining_gates': state['remaining_freeze_gates'], 'freeze_authorized': False, 'frozen': False,
        'semantic_extraction_run': False, 'plan_thresholds_changed': False, 'plan_limits_changed': False, 'forbidden_work_performed': [],
    }
    save('completion-after-decision-05.json', completion)
    measurement = P / 'measurement/M-POC1C-review-006'
    measurement.mkdir()
    with (measurement / 'completion.json').open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(completion, ensure_ascii=False, indent=2) + '\n')
    save('closure-seal-after-decision-05.json', {
        'recorded_at_utc': now, 'card': 'M-POC1C', 'outcome': 'partial', 'workflow_status': 'waiting_review', 'frozen': False,
        'review_manifest': ref(HERE / 'review-manifest-after-decision-05.json'), 'completion': ref(HERE / 'completion-after-decision-05.json'),
        'measurement_completion': ref(measurement / 'completion.json'), 'public_documents': [ref(ROOT / name) for name in (*ALLOWED, HANDOFF)],
        'next_question': state['next_question'], 'counts': state['counts'], 'no_self_hash_cycle': True,
    })
    print(json.dumps({'seal': ref(HERE / 'closure-seal-after-decision-05.json'), 'preserved_files': len(preserved), 'checks': '92 passed'}, indent=2))
else:
    raise SystemExit('Use record or close CHECK_ROOT.')
