"""Append partial closure after the first real owner decision in M-POC1C."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
HERE = Path(__file__).resolve().parent
P = ROOT / 'private/poc/spqr-chapter9'
C = P / 'evaluation/eval-v1-candidate-20261008-02'
CHECK = ROOT / 'private/poc/_checks/active-8854bbb141eb4bc78ebfe18110e51a5a'
MEASUREMENT = P / 'measurement/M-POC1C-review-002'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ref(path):
    with path.open('rb') as stream:
        sha256 = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':sha256,'bytes':path.stat().st_size}


def save(path, value):
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


baseline = read(HERE / 'baseline.json')
unchanged, intentional = [], []
for item in baseline['files']:
    actual = ref(ROOT / item['path'])
    if item != actual:
        assert item['path'] in baseline['allowed_public_updates'], (item,actual)
        intentional.append({'before':item,'after':actual})
    else:
        unchanged.append(actual)
candidate = read(C / 'manifest.json')
for item in [*candidate['artifacts'],*candidate['provenance']]:
    assert ref(ROOT / item['path']) == item, item
decision = read(HERE / 'decision-01-DEP008.json')
overlay = read(HERE / 'dependency-overlay-01.json')
state = read(HERE / 'review-state-after-decision-01.json')
assert overlay['authorizing_decision'] == ref(HERE / 'decision-01-DEP008.json')
assert decision['raw_response'] == ref(HERE / 'owner-answer-01.raw.txt')
assert decision['actual_owner_response'] == 'Tak zatwierdzam'
assert not decision['freeze_authorized']
relations = [*read(C / 'dependencies.json')['confirmed_execution_relations'],overlay['confirmed_relation']]
assert len({(row['from'],row['to'],row['kind'],row['explicitness']) for row in relations}) == 4
assert len([row for row in relations if row['explicitness'] == 'explicit']) == 1
assert state['counts']['confirmed_explicit_execution'] == 1
assert sum(state['counts'][key] for key in ('confirmed_explicit_execution','confirmed_implicit_execution','unconfirmed_explicit_execution','unconfirmed_implicit_execution','mentions_separate','continuations_separate')) == 127
assert not (P / 'evaluation/eval-v1').exists() and not (P / 'evaluation/freeze-public-v1.json').exists()
check_result = read(CHECK / 'result.json')
assert check_result['tests_exit'] == check_result['diff_exit'] == 0
assert '88 passed' in (CHECK / 'pytest.log').read_text(encoding='utf-8-sig')
git_env = {**os.environ,'GIT_OPTIONAL_LOCKS':'0'}
git_prefix = ['git','-c','safe.directory=C:/dev/wargame-compiler']
diff = subprocess.run([*git_prefix,'diff','--check'],cwd=ROOT,env=git_env,capture_output=True,text=True)
assert diff.returncode == 0
head = subprocess.run([*git_prefix,'rev-parse','HEAD'],cwd=ROOT,env=git_env,check=True,capture_output=True,text=True).stdout.strip()
assert head == '90535261a4498cabcd6abc0af33b56a4267b6193'
now = datetime.now(timezone.utc).isoformat()
files = [ref(HERE / name) for name in (
    'baseline.json','owner-answer-01.raw.txt','decision-01-DEP008.json','dependency-overlay-01.json',
    'change-map-decision-01.json','pending-question-02-DEP002.json','review-state-after-decision-01.json','record.py','close.py')]
save(HERE / 'review-manifest-after-decision-01.json',{
    'recorded_at_utc':now,'card':'M-POC1C','outcome':'partial','workflow_status':'waiting_review',
    'base_candidate':ref(C / 'manifest.json'),'files':files,
    'previous_closure':ref(P / 'evaluation/M-POC1C-review-001/closure-seal.json'),
    'actual_owner_decisions':1,'counts':state['counts'],'frozen':False,'freeze_authorized':False,
})
completion = {
    'id':'M-POC1C-review-002-after-decision-01','recorded_at_utc':now,'date':'2026-10-08',
    'timezone':'Europe/Warsaw','card':'M-POC1C','outcome':'partial','workflow_status':'waiting_review',
    'milestone':'M-POC1','milestone_status':'next','next_card':'M-POC1C',
    'branch':'feature/tests','head':head,
    'decision':ref(HERE / 'decision-01-DEP008.json'),'review_manifest':ref(HERE / 'review-manifest-after-decision-01.json'),
    'candidate_and_overlays':{'candidate':ref(C / 'manifest.json'),'overlays_in_order':[ref(HERE / 'dependency-overlay-01.json')]},
    'source':ref(P / 'source/original-pdf-20261008-01.pdf'),'counts':state['counts'],
    'situations':state['situations'],'pending_question':ref(HERE / 'pending-question-02-DEP002.json'),
    'freeze_authorized':False,'frozen':False,'semantic_extraction_run':False,'MPOC2A_executed':False,'MPOC2B_executed':False,
    'checks':{'scripts_check':'88 passed','result':check_result,'local_TMP_TEMP':str(CHECK / 'temp'),
              'new_basetemp':True,'logs':[ref(CHECK / 'pytest.log'),ref(CHECK / 'result.json')],
              'final_git_diff_check':{'exit':diff.returncode,'stdout':diff.stdout,'stderr':diff.stderr}},
    'preservation':{'baseline_checked':len(baseline['files']),'unchanged':len(unchanged),
                    'intentional_public_updates':intentional,'preserved_files':unchanged,
                    'prior_candidate_manifests_and_history_unchanged':True,
                    'historical_Git_snapshot_restore_performed':False},
    'measurement':{'model_selector_owner_report':'sol','exact_model_version':'unknown','reasoning_selector':'unknown',
                   'active_work_time':'unknown','user_active_time':'unknown','tokens':'unknown','cost':'unknown',
                   'calendar_time_is_active_work':False},
    'remaining_gates':state['remaining_freeze_gates'],'quality_metrics':'n/a: no freeze or extractor response',
    'plan_thresholds_changed':False,'plan_limits_changed':False,'forbidden_work_performed':[],
}
save(HERE / 'completion-after-decision-01.json',completion)
MEASUREMENT.mkdir()
save(MEASUREMENT / 'completion.json',completion)
save(HERE / 'closure-seal-after-decision-01.json',{
    'recorded_at_utc':now,'card':'M-POC1C','outcome':'partial','workflow_status':'waiting_review','frozen':False,
    'review_manifest':ref(HERE / 'review-manifest-after-decision-01.json'),
    'completion':ref(HERE / 'completion-after-decision-01.json'),
    'measurement_completion':ref(MEASUREMENT / 'completion.json'),
    'public_documents':[ref(ROOT / name) for name in ('docs/STATUS.md','docs/ROADMAP.md','docs/HANDOFF.md','docs/handoff/2026-10-08-M-POC1C-review-002.md')],
    'next_question':'M-POC1C-RQ-02-DEP002','counts':state['counts'],'no_self_hash_cycle':True,
})
print(json.dumps({'decision':ref(HERE / 'decision-01-DEP008.json'),
                  'seal':ref(HERE / 'closure-seal-after-decision-01.json'),
                  'prior_files_unchanged':len(unchanged),'test_result':'88 passed','diff_check':diff.returncode},indent=2))
