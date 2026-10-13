"""Record owner assent and refreshed assignment before review."""
from pathlib import Path
from datetime import datetime,timezone
from collections import Counter
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';D=ROOT/'docs';PACK=R/'part-04d2';PRE=P/'measurement/M-POC5A-semantic-04d2'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();C=load(R/'checklist.json');prior=load(R/'current-state-24.json');packet=load(PACK/'comparisons.json');pres=load(PACK/'presentation.json');planpath=P/'measurement/M-POC5A-semantic-04d1/scope-plan.json';plan=load(planpath);ids=plan['parts'][2]['inventory_ids'];assert len(ids)==59
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl'];types=Counter(x['type'] for x in C['inventory'] if x['id'] in ids)
save(M/'start.json',dict(card='M-POC5A.4d3',recorded_at_utc=now,protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),prior_state=ref(R/'current-state-24.json'),estimate_before_semantic_review=dict(refreshed_minutes_range=[75,90],assigned_inventory_ids=59,assigned_occurrences=118,inventory_types=dict(types),basis='Coherent supplied pages34–35, precise source clauses and selected fields/graphic; earlier scoped judgments retained. No full situation execution or unspecified-field certificate.',fits_single90min_session=True,only_current_part=True,further_split_before_execution_if_estimate_exceeds90=True),active_time='unknown',model_selector='unknown',reasoning_selector='unknown'))
for x in [C['source'],C['evaluation'],*C['responses'].values(),*load(PACK/'manifest.json')['artifacts']]:assert ref(ROOT/x['path'])==x
save(M/'scope-assignment.json',dict(card='M-POC5A.4d3',original_before_review_plan=ref(planpath),part_pointer='/parts/2',assigned_ids=ids,assigned_occurrences=118,before_semantic_review=True,estimate=ref(M/'start.json')))
reply='Zatwierdzam i kontynuuj';reviewer='owner in this chat; personal identity unknown'
save(M/'approval-evidence.json',dict(owner_reply_verbatim=reply,recorded_at_utc=now,owner_message_sent_at_utc='unknown',actual_owner_file_open_or_read='unknown',interpretation='Accept immediately presented.4d2:136 bounded label/clause/row/glyph/orientation/physical-continuation assessments. Older minimum1,specificcommandexceptions,compass,rating meanings and other unresolved remain open. Continue next.4d3.',presented_decisions=pres['decisions'],basis=[ref(PACK/'owner-focus.md'),ref(PACK/'presentation.json')]))
scopes=[]
for i,row in enumerate(packet['inventory']):
    j=copy.deepcopy(row);j.update(status='reviewed',human_reviewer=reviewer,reviewer=reviewer,recorded_at_utc=now,whole_record_accepted=False,comparison_artifact=ref(PACK/'comparisons.json'),comparison_pointer=f'/inventory/{i}')
    for run,x in j['runs'].items():x.update(status='reviewed',human_reviewer=reviewer,reviewer=reviewer,owner_decision='accepted_presented_bounded_assessment',whole_record_accepted=False)
    scopes.append(j)
decision=dict(id='M-POC5A-owner-decision-12',card='M-POC5A',part='M-POC5A.4d2',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,reviewer=reviewer,owner_reply_verbatim=reply,decision='accepted_presented136_bounded_inventory_assessments',approval_evidence=ref(M/'approval-evidence.json'),prior_decision=ref(R/'owner-decision-11.json'),prior_state=ref(R/'current-state-24.json'),comparison_manifest=ref(PACK/'manifest.json'),focused_packet=ref(PACK/'owner-focus.md'),evaluation=C['evaluation'],responses=C['responses'],source=C['source'],recommendations=pres['decisions'],scopes=scopes,newly_reviewed_inventory_occurrences=136,per_answer={'first-001':68,'context-01':68},bounded_supported_occurrences=136,issue_disposition={},unresolved_prior_issue_ids=prior['unresolved_issue_ids'],pending_expectation_ids=prior['pending_expectation_ids'],count_policy=packet['scope_policy'],owner_file_open_or_read='unknown',metrics='not_assessable',excluded=pres['excludes'],no_response_changes=True,no_gold_change=True,no_new_sources=True,whole_card_closed=False)
save(R/'owner-decision-12.json',decision);dr=ref(R/'owner-decision-12.json');oldo=load(R/'owner-review-overlay-11.json');o=copy.deepcopy(oldo)
o.update(id='M-POC5A-owner-review-overlay-12',decision=dr,prior_overlay=ref(R/'owner-review-overlay-11.json'),inventory_owner_decision=dr,owner_reviewed_inventory_scoped_occurrences=214,inventory_count_policy=packet['scope_policy'])
for run,v in o['runs'].items():
    v['inventory_scopes'] += [dict(id=j['id'],source_scopes=j['source_scopes'],manual_assessment=j['manual_assessment'],comparison=j['manual_comparison'],decision=dr,trace=j['runs'][run],status='reviewed',reviewer=reviewer,whole_record_accepted=False) for j in scopes];v['owner_reviewed_inventory_scoped_occurrences']=107
save(R/'owner-review-overlay-12.json',o)
(R/'owner-review-summary-12.md').write_text('# Zatwierdzenie .4d2\n\nWłaściciel: „'+reply+'”. Przyjęto136 dokładnych ocen oznaczeń/klauzul/tabeli/grafiki/fizycznych kontynuacji, nie pełne rekordy lub nowe punkty rubryki. Starsze13kwestii/8oczekiwań i rating meanings/kompas/minimum1/wyjątki dowodzenia nadalotwarte. Oryginały bez naprawy. Łącznie214 zakresów inwentarza z decyzjami; kolejna.4d3 59pozycji118wystąpień.\n',encoding='utf-8')
s=copy.deepcopy(prior);s.update(id='M-POC5A-current-state-25',part='M-POC5A.4d2-owner-review',previous_state=ref(R/'current-state-24.json'),decision=dr,overlay=ref(R/'owner-review-overlay-12.json'),inventory_owner_decision=dr,new_owner_decisions=[dr],part_4d2_owner_review_complete=True,inventory_owner_reviewed_new_occurrences=136,inventory_owner_reviewed_assigned_occurrences=214,inventory_owner_pending_compared_occurrences=0,next_part='M-POC5A.4d3',next_action='Execute only.4d3 assigned59IDs118occurrences after refreshed75–90minute estimate. Remaining41IDs and.4d5 reconciliation separate, old unresolved preserved.',resume='Owner12 accepted136 bounded.4d2 facets;214 total assigned inventory occurrence scopes owner-reviewed. Next.4d3 only.')
s['summary'].update(new_owner_reviewed_occurrences=136,owner_pending_occurrences=0,owner_accepted_scoped_occurrences=136);save(R/'current-state-25.json',s)
save(M/'owner-decision-artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-12.json','owner-review-overlay-12.json','current-state-25.json','owner-review-summary-12.md']]))
paths=[ROOT/x['path'] for x in load(PRE/'read-inputs.json')['files']]+[R/'current-state-24.json',R/'current-state-25.json',R/'owner-decision-12.json',R/'owner-review-overlay-12.json',PACK/'comparisons.json',PACK/'manifest.json',D/'handoff/2026-10-11-M-POC5A-semantic-04d2.md',D/'work/tasks/semantic/M-POC5A.4d3.md'];paths=list(dict.fromkeys(paths))
for path in paths:
    b=path.read_bytes();json.loads(b) if path.suffix=='.json' else b.decode('utf-8-sig')
save(M/'read-inputs.json',dict(files=[ref(p) for p in paths],method='Full bytes read/JSON parsed for required inputs; source/content manual comparisons separately. User localC:/repo overrides stale bootstrapC:/dev.'))
public=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4d','.4d2','.4d3']]];save(M/'public-documents-before.json',[ref(p) for p in public])
print(json.dumps(dict(assigned_ids=59,occurrences=118,types=dict(types),estimate=[75,90],protected=len(protected),owner_accepted_previous=136,owner_inventory_total=214)))
