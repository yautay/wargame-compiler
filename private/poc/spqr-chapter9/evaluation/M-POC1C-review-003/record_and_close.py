"""Append decision 02 and its audit; invoked separately before/after checks."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
HERE = Path(__file__).resolve().parent
PREVIOUS = P / 'evaluation/M-POC1C-review-002'
C = P / 'evaluation/eval-v1-candidate-20261008-02'
ALLOWED = ['docs/STATUS.md','docs/ROADMAP.md','docs/HANDOFF.md']


def load(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ref(path):
    with path.open('rb') as stream:
        sha = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path':path.relative_to(ROOT).as_posix(),'sha256':sha,'bytes':path.stat().st_size}


def save(name,value):
    path = HERE / name
    with path.open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(value,ensure_ascii=False,indent=2)+'\n')


def git(*args):
    return subprocess.run(['git','-c','safe.directory=C:/dev/wargame-compiler',*args],cwd=ROOT,
                          env={**os.environ,'GIT_OPTIONAL_LOCKS':'0'},capture_output=True,text=True,check=True).stdout.strip()


now = datetime.now(timezone.utc).isoformat()
assert git('branch','--show-current') == 'feature/tests'
git('merge-base','--is-ancestor','90535261a4498cabcd6abc0af33b56a4267b6193','HEAD')
head = git('rev-parse','HEAD')
assert not (P / 'evaluation/eval-v1').exists() and not (P / 'evaluation/freeze-public-v1.json').exists()
candidate = load(C / 'manifest.json')
for item in [*candidate['artifacts'],*candidate['provenance']]:
    assert ref(ROOT / item['path']) == item, item

if sys.argv[1] == 'record':
    seal = load(PREVIOUS / 'closure-seal-after-decision-01.json')
    for item in [seal['review_manifest'],seal['completion'],seal['measurement_completion'],*seal['public_documents']]:
        assert ref(ROOT / item['path']) == item, item
    paths = {ROOT / r['path'] for r in load(PREVIOUS / 'baseline.json')['files']}
    paths.update(path for path in PREVIOUS.iterdir() if path.is_file())
    paths.update(path for path in C.iterdir() if path.is_file())
    paths.add(ROOT / 'docs/handoff/2026-10-08-M-POC1C-review-002.md')
    save('baseline.json',{'recorded_at_utc':now,'files':[ref(path) for path in sorted(paths)],'allowed_public_updates':ALLOWED})
    question = load(PREVIOUS / 'pending-question-02-DEP002.json')
    assert (HERE / 'owner-answer-02.raw.txt').read_text(encoding='utf-8').rstrip('\n') == 'zatwierdzam'
    decision = {
        'id':'M-POC1C-owner-decision-02','card':'M-POC1C','question_id':question['id'],
        'date':'2026-10-09','date_source':'client time context','timezone':'Europe/Warsaw',
        'recorded_at_utc':now,'user_message_timestamp':'unknown','reviewer':'owner in this chat; no personal identity attributed',
        'actual_owner_response':'zatwierdzam','raw_response':ref(HERE / 'owner-answer-02.raw.txt'),
        'capture_method':'Verbatim user message copied from this conversation with a terminal LF.',
        'approved_question':'Czy zatwierdzasz to powiązanie jako kolejny element oceny?',
        'shown_proposal':'9.11 korzysta z reguły Rampage 9.14, ponieważ przesunięcie słonia do tylnego heksu obrońcy wymaga, żeby słoń nie wpadł w Rampage.',
        'shown_source_excerpt':question['shown_source_excerpt'],
        'approved_scope':{**question['proposed_tuple'],'necessity_scope':question['plain_language_proposal'],
                          'target_scope':'Absence of Rampage for this placement only; full Rampage outcomes are not collectively certified.',
                          'remaining_conditions':question['remaining_conditions']},
        'criticality':'critical in previously approved local placement scope',
        'criticality_basis':ref(P / 'evaluation/owner-review-002/decision-04-RQ-03.json'),
        'new_separate_criticality_statement_by_owner':False,
        'basis':[ref(PREVIOUS / 'pending-question-02-DEP002.json'),ref(C / 'manifest.json'),
                 ref(P / 'evaluation/draft/dependencies.json')],
        'not_approved':['Other proposed relation tuples','Full external procedures, map/parameters','All 9.14 clauses together',
                        'Scoring grouping/rubrics','eval-v1 freeze','M-POC2A/B'],
        'new_situations':[],'freeze_authorized':False,'frozen':False,
    }
    save('decision-02-DEP002.json',decision)
    counts = {'confirmed_explicit_execution':2,'confirmed_implicit_execution':3,
              'unconfirmed_explicit_execution':97,'unconfirmed_implicit_execution':11,
              'mentions_separate':7,'continuations_separate':7,'parent_facets':127}
    save('dependency-overlay-02.json',{
        'id':'M-POC1C-dependency-overlay-02','authorizing_decision':ref(HERE / 'decision-02-DEP002.json'),
        'base_candidate_manifest':ref(C / 'manifest.json'),
        'previous_overlay':ref(PREVIOUS / 'dependency-overlay-01.json'),
        'operation':'add DEP-002 in confirmed set and remove it from unconfirmed set during materialization',
        'confirmed_relation':{**decision['approved_scope'],'executable':True,'target_status':'internal',
                              'review_status':'owner_confirmed_exact_scope','criticality':decision['criticality'],
                              'criticality_basis':decision['criticality_basis'],
                              'source_evidence':question['source_evidence'],'target_evidence':question['target_evidence'],
                              'owner_decision':ref(HERE / 'decision-02-DEP002.json')},
        'counts_after_overlay':counts,'original_artifacts_modified':[],'freeze_authorized':False,
    })
    save('change-map-decision-02.json',{
        'decision':ref(HERE / 'decision-02-DEP002.json'),'overlay':ref(HERE / 'dependency-overlay-02.json'),
        'parent':ref(C / 'manifest.json'),'id':'DEP-002',
        'from':'unconfirmed_relation_fields','to':'owner_confirmed_explicit_local_condition',
        'counts_delta':{'confirmed_explicit_execution':1,'unconfirmed_explicit_execution':-1},'original_artifacts_modified':[],
    })
    dependencies = load(P / 'evaluation/draft/dependencies.json')
    next_dep = next(row for row in dependencies['dependencies'] if row['id']=='DEP-017')
    inventory = load(P / 'evaluation/draft/inventory.json')
    target = next(row for row in inventory['items'] if row['id']=='C-9.41-01')
    save('pending-question-03-DEP017.json',{
        'id':'M-POC1C-RQ-03-DEP017','status':'waiting_owner_decision','source_evidence':next_dep['evidence'][0],
        'target_evidence':target['evidence'][0],
        'shown_source_excerpt':'Phalanx Defense (9.41) also applies.',
        'plain_language_proposal':'9.53 invokes Phalanx Defense from 9.41 for defending Double Depth only when the conditions of 9.41 hold; it does not grant the defensive CRT shift unconditionally.',
        'proposed_tuple':{key:next_dep[key] for key in ('id','from','to','kind','explicitness')},
        'criticality_basis':ref(P / 'evaluation/owner-review-002/decision-08-RQ-07.json'),
        'scope_limits':'Local invocation and retained target conditions only; actual CRT/geometry and full game outcome unclosed.',
        'actual_owner_answer':None,'freeze_authorization_requested':False,
    })
    save('review-state-after-decision-02.json',{
        'recorded_at_utc':now,'date':'2026-10-09','card':'M-POC1C','result':'partial','workflow_status':'waiting_review',
        'base_candidate':ref(C / 'manifest.json'),'overlays_in_order':[ref(PREVIOUS / 'dependency-overlay-01.json'),ref(HERE / 'dependency-overlay-02.json')],
        'actual_owner_decisions':2,'counts':counts,'confirmed_execution_ids':['DEP-008','DEP-002','DEP-NEW-001','DEP-NEW-002','DEP-NEW-003'],
        'situations':{'total':20,'local_results':17,'blocks':3,'new':0},
        'remaining_internal_explicit_tuple_questions':['DEP-017','DEP-024','DEP-041'],
        'remaining_freeze_gates':['Needed relation scopes','Scoring grouping/category rubrics and retained limitations','Distinct actual owner freeze decision'],
        'next_question':'M-POC1C-RQ-03-DEP017','milestone':'M-POC1','milestone_status':'next','next_card':'M-POC1C',
        'freeze_authorized':False,'frozen':False,
    })
    print(json.dumps({'decision':ref(HERE / 'decision-02-DEP002.json'),'counts':counts},indent=2))
elif sys.argv[1] == 'close':
    check_root = (ROOT / sys.argv[2]).resolve()
    assert check_root.is_relative_to((ROOT / 'private/poc/_checks').resolve())
    result = load(check_root / 'result.json')
    assert result['tests_exit']==result['diff_exit']==0
    pytest_log = (check_root / 'pytest.log').read_text(encoding='utf-8-sig')
    assert '89 passed' in pytest_log
    baseline = load(HERE / 'baseline.json')
    preserved,changed = [],[]
    for item in baseline['files']:
        actual = ref(ROOT / item['path'])
        if item != actual:
            assert item['path'] in ALLOWED, (item,actual)
            changed.append({'before':item,'after':actual})
        else:
            preserved.append(actual)
    state = load(HERE / 'review-state-after-decision-02.json')
    relations = [*load(C / 'dependencies.json')['confirmed_execution_relations']]
    for item in state['overlays_in_order']:
        assert ref(ROOT / item['path'])==item
        overlay = load(ROOT / item['path'])
        assert ref(ROOT / overlay['authorizing_decision']['path'])==overlay['authorizing_decision']
        relations.append(overlay['confirmed_relation'])
    assert len({(r['from'],r['to'],r['kind'],r['explicitness']) for r in relations})==5
    assert len([r for r in relations if r['explicitness']=='explicit'])==2
    assert sum(state['counts'][key] for key in state['counts'] if key!='parent_facets')==127
    git('diff','--check')
    files = [ref(path) for path in sorted(HERE.iterdir()) if path.is_file()]
    save('review-manifest-after-decision-02.json',{'recorded_at_utc':now,'card':'M-POC1C','status':'partial/waiting_review',
                                               'files':files,'base_candidate':ref(C / 'manifest.json'),
                                               'previous_closure':ref(PREVIOUS / 'closure-seal-after-decision-01.json'),
                                               'counts':state['counts'],'frozen':False})
    completion = {'id':'M-POC1C-review-003-after-decision-02','recorded_at_utc':now,'date':'2026-10-09','timezone':'Europe/Warsaw',
                  'card':'M-POC1C','outcome':'partial','workflow_status':'waiting_review','milestone':'M-POC1','milestone_status':'next','next_card':'M-POC1C',
                  'branch':'feature/tests','head':head,'decision':ref(HERE / 'decision-02-DEP002.json'),
                  'review_manifest':ref(HERE / 'review-manifest-after-decision-02.json'),
                  'candidate_and_overlays':{'candidate':ref(C / 'manifest.json'),'overlays_in_order':state['overlays_in_order']},
                  'counts':state['counts'],'situations':state['situations'],'pending_question':ref(HERE / 'pending-question-03-DEP017.json'),
                  'checks':{'scripts_check':'89 passed','result':result,'local_TMP_TEMP':str(check_root / 'temp'),'new_basetemp':True,
                            'logs':[ref(check_root / 'pytest.log'),ref(check_root / 'result.json')],'final_git_diff_check_exit':0},
                  'preservation':{'baseline_checked':len(baseline['files']),'unchanged':len(preserved),'preserved_files':preserved,'intentional_public_updates':changed},
                  'measurement':{'model_selector_owner_report':'sol','exact_model_version':'unknown','reasoning_selector':'unknown','active_work_time':'unknown',
                                 'user_active_time':'unknown','tokens':'unknown','cost':'unknown','calendar_time_is_active_work':False},
                  'remaining_gates':state['remaining_freeze_gates'],'freeze_authorized':False,'frozen':False,'semantic_extraction_run':False,
                  'plan_thresholds_changed':False,'plan_limits_changed':False,'forbidden_work_performed':[]}
    save('completion-after-decision-02.json',completion)
    measurement = P / 'measurement/M-POC1C-review-003'
    measurement.mkdir()
    with (measurement / 'completion.json').open('x',encoding='utf-8',newline='\n') as stream:
        stream.write(json.dumps(completion,ensure_ascii=False,indent=2)+'\n')
    save('closure-seal-after-decision-02.json',{'recorded_at_utc':now,'card':'M-POC1C','outcome':'partial','workflow_status':'waiting_review','frozen':False,
         'review_manifest':ref(HERE / 'review-manifest-after-decision-02.json'),'completion':ref(HERE / 'completion-after-decision-02.json'),
         'measurement_completion':ref(measurement / 'completion.json'),
         'public_documents':[ref(ROOT / name) for name in (*ALLOWED,'docs/handoff/2026-10-09-M-POC1C-review-003.md')],
         'next_question':state['next_question'],'counts':state['counts'],'no_self_hash_cycle':True})
    print(json.dumps({'seal':ref(HERE / 'closure-seal-after-decision-02.json'),'preserved_files':len(preserved),'checks':'89 passed'},indent=2))
else:
    raise SystemExit('Use record or close CHECK_ROOT.')
