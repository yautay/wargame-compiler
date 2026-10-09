"""Record a real M-POC1C owner decision and an additive evaluation overlay."""
from __future__ import annotations

import hashlib
import json
import os
import subprocess
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
P = ROOT / 'private/poc/spqr-chapter9'
HERE = Path(__file__).resolve().parent
PREVIOUS = P / 'evaluation/M-POC1C-review-001'
CANDIDATE = P / 'evaluation/eval-v1-candidate-20261008-02'
DRAFT = P / 'evaluation/draft'


def read(path):
    return json.loads(path.read_text(encoding='utf-8-sig'))


def ref(path):
    with path.open('rb') as stream:
        sha256 = hashlib.file_digest(stream, 'sha256').hexdigest()
    return {'path': path.relative_to(ROOT).as_posix(), 'sha256': sha256, 'bytes': path.stat().st_size}


def save(path, value):
    with path.open('x', encoding='utf-8', newline='\n') as stream:
        stream.write(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


if (HERE / 'decision-01-DEP008.json').exists():
    raise SystemExit('Decision exists; refusing to overwrite.')
now = datetime.now(timezone.utc).isoformat()
git_env = {**os.environ, 'GIT_OPTIONAL_LOCKS':'0'}
git_prefix = ['git','-c','safe.directory=C:/dev/wargame-compiler']
branch = subprocess.run([*git_prefix,'branch','--show-current'],cwd=ROOT,env=git_env,check=True,capture_output=True,text=True).stdout.strip()
head = subprocess.run([*git_prefix,'rev-parse','HEAD'],cwd=ROOT,env=git_env,check=True,capture_output=True,text=True).stdout.strip()
assert branch == 'feature/tests'
assert head == '90535261a4498cabcd6abc0af33b56a4267b6193'
previous_seal = read(PREVIOUS / 'closure-seal.json')
for item in [previous_seal['candidate_manifest'],previous_seal['completion'],previous_seal['measurement_completion'],*previous_seal['public_documents'],*previous_seal['scripts']]:
    assert ref(ROOT / item['path']) == item, item
candidate = read(CANDIDATE / 'manifest.json')
for item in [*candidate['artifacts'],*candidate['provenance']]:
    assert ref(ROOT / item['path']) == item, item
baseline_paths = {ROOT / item['path'] for item in read(PREVIOUS / 'baseline.json')['files']}
baseline_paths.update(path for path in PREVIOUS.iterdir() if path.is_file())
baseline_paths.update(path for path in CANDIDATE.iterdir() if path.is_file())
baseline_paths.add(ROOT / 'docs/handoff/2026-10-08-M-POC1C-review-001.md')
save(HERE / 'baseline.json',{'recorded_at_utc':now,'files':[ref(path) for path in sorted(baseline_paths)],
                          'allowed_public_updates':['docs/STATUS.md','docs/ROADMAP.md','docs/HANDOFF.md']})
assert (HERE / 'owner-answer-01.raw.txt').read_text(encoding='utf-8').rstrip('\n') == 'Tak zatwierdzam'
decision = {
    'id':'M-POC1C-owner-decision-01', 'card':'M-POC1C', 'question_id':'M-POC1C-RQ-01-DEP008',
    'date':'2026-10-08','timezone':'Europe/Warsaw','recorded_at_utc':now,
    'user_message_timestamp':'unknown','reviewer':'owner in this chat; no personal identity attributed',
    'actual_owner_response':'Tak zatwierdzam','raw_response':ref(HERE / 'owner-answer-01.raw.txt'),
    'raw_capture_method':'Exact user text copied from this conversation; file has a terminal LF, not an original downloaded file.',
    'preceding_owner_clarification':'Nie rozumiem ?',
    'clarified_question': 'Czy zatwierdzasz taki element oceny: „9.24 ustanawia dla SK wyjątek od końcowego testu Pass-Thru opisanego w 9.11”?',
    'shown_explanation': '9.11 describes the final Pass-Thru test; 9.24 exempts SK. The link will be used as a comparison standard to check whether extraction ties the exception to its test. Losing the exception could wrongly require a SK test.',
    'approved_scope':{
        'id':'DEP-008','from':'C-9.24-03','to':'C-9.11-10','kind':'exception','explicitness':'explicit',
        'original_target_reference':'9.11','target_refinement':'Final Pass-Thru TQ check in step 4, not the whole 9.11 procedure.',
        'necessity_scope':'Preserve the SK exemption from that final check only.',
        'source_evidence':'The quoted 9.24 sentence explicitly references (9.11); the shown step 4 excludes a Skirmisher unit.',
        'criticality':'critical in this scope: omitting exception changes whether the final test is required',
        'criticality_attribution':'Concrete consequence was shown in the clarification and accepted; the technical label is a mapping under POC-PLAN, not claimed as a verbatim owner statement.',
    },
    'basis':[ref(PREVIOUS / 'pending-question.json'),ref(CANDIDATE / 'manifest.json'),
             ref(DRAFT / 'dependencies.json'),ref(DRAFT / 'inventory.json'),
             ref(P / 'evaluation/owner-review-002/decision-04-RQ-03.json')],
    'not_approved':['Other TQ tests','Full external Pre-Shock/Shock procedure','Other proposed relation fields or aliases',
                    'All expectations/relations collectively','Scoring grouping/categories','eval-v1 freeze','M-POC2A/B'],
    'new_situations':[], 'situation_changes':[], 'freeze_authorized':False, 'frozen':False,
}
save(HERE / 'decision-01-DEP008.json',decision)
draft_dependencies = read(DRAFT / 'dependencies.json')
draft_map = {row['id']:row for row in draft_dependencies['dependencies']}
old_dep = draft_map['DEP-008']
question = read(PREVIOUS / 'pending-question.json')
overlay = {
    'id':'M-POC1C-dependency-overlay-01','authorizing_decision':ref(HERE / 'decision-01-DEP008.json'),
    'base_candidate_manifest':ref(CANDIDATE / 'manifest.json'),
    'original_parent':{**ref(DRAFT / 'dependencies.json'),'id':'DEP-008'},
    'operation':'add one scoped confirmed explicit execution relation; remove it from the unconfirmed set when materializing',
    'confirmed_relation':{
        **decision['approved_scope'],'executable':True,'target_status':'internal',
        'review_status':'owner_confirmed_exact_scope','source_evidence':question['source_quote'],
        'target_evidence':question['target_quote'],'owner_decision':ref(HERE / 'decision-01-DEP008.json'),
    },
    'counts_after_overlay':{'confirmed_explicit_execution':1,'confirmed_implicit_execution':3,
                           'unconfirmed_explicit_execution':98,'unconfirmed_implicit_execution':11,
                           'mentions_separate':7,'continuations_separate':7,'parent_facets':127},
    'original_artifacts_modified':[], 'no_freeze':True,
}
save(HERE / 'dependency-overlay-01.json',overlay)
save(HERE / 'change-map-decision-01.json',{
    'decision':ref(HERE / 'decision-01-DEP008.json'),'overlay':ref(HERE / 'dependency-overlay-01.json'),
    'parents':[ref(CANDIDATE / 'manifest.json'),ref(DRAFT / 'dependencies.json')],
    'operations':[{'id':'DEP-008','from':'unconfirmed_relation_fields','to':'owner_confirmed_explicit_local_exception',
                   'scope':decision['approved_scope']}], 'original_artifacts_modified':[],
    'counts_delta':{'confirmed_explicit_execution':1,'unconfirmed_explicit_execution':-1},
})
next_dep = draft_map['DEP-002']
inventory = read(DRAFT / 'inventory.json')
target = next(row for row in inventory['items'] if row['id'] == 'R-9.14')
save(HERE / 'pending-question-02-DEP002.json',{
    'id':'M-POC1C-RQ-02-DEP002','status':'waiting_owner_decision','topic':'one remaining explicit relation scope',
    'source_evidence':next_dep['evidence'][0],'target_evidence':target['evidence'][0],
    'shown_source_excerpt':'if the infantry unit did not rout and the Elephant unit has not rampaged (9.14)',
    'plain_language_proposal':'9.11 uses 9.14 to check absence of Elephant Rampage before the stated post-Pass-Thru placement.',
    'proposed_tuple':{key:next_dep[key] for key in ('id','from','to','kind','explicitness')},
    'proposed_criticality':'critical: omitting the gate could incorrectly permit the post-Shock placement',
    'remaining_conditions':'Infantry not routed, free Rear, Elephant player choice and unchanged facing remain required; no invented Rampage outcome or external Rout procedure.',
    'actual_owner_answer':None,'freeze_authorization_requested':False,
})
save(HERE / 'review-state-after-decision-01.json',{
    'recorded_at_utc':now,'card':'M-POC1C','result':'partial','workflow_status':'waiting_review',
    'base_candidate':ref(CANDIDATE / 'manifest.json'),'overlays_in_order':[ref(HERE / 'dependency-overlay-01.json')],
    'actual_owner_decisions':1,'confirmed_execution_ids':['DEP-008','DEP-NEW-001','DEP-NEW-002','DEP-NEW-003'],
    'counts':overlay['counts_after_overlay'], 'situations':{'total':20,'local_results':17,'blocks':3,'new':0},
    'remaining_internal_explicit_tuple_questions':['DEP-002','DEP-017','DEP-024','DEP-041'],
    'remaining_freeze_gates':['Needed explicit relation scopes','Scoring grouping/category rubrics and retained limitations','Distinct actual owner freeze decision'],
    'next_question':'M-POC1C-RQ-02-DEP002','milestone':'M-POC1','milestone_status':'next',
    'next_card':'M-POC1C','freeze_authorized':False,'frozen':False,
})
print(json.dumps({'decision':ref(HERE / 'decision-01-DEP008.json'),
                  'overlay':ref(HERE / 'dependency-overlay-01.json'),
                  'counts':overlay['counts_after_overlay']},indent=2))
