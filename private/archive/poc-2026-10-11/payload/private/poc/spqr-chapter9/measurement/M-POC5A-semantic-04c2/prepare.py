"""Record exact locator assent and estimate next assigned part before review."""
from pathlib import Path
from datetime import datetime,timezone
import copy,json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';PACK=R/'part-04c1';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();C=load(R/'checklist.json');prior=load(R/'current-state-16.json');packet=load(PACK/'comparisons.json');pres=load(PACK/'presentation.json')
planpath=P/'measurement/M-POC5A-semantic-04c1/scope-plan.json';plan=load(planpath);assigned=plan['parts'][1];assert assigned['occurrences']==42
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(card='M-POC5A.4c2',recorded_at_utc=now,protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),prior_state=ref(R/'current-state-16.json'),
    estimate_before_locator_review=dict(minutes_range=[60,80],assigned_ids=21,assigned_occurrences=42,further_split_required=False,includes_recording_previous_bounded_assent=True),
    scope_plan=ref(planpath),active_time='unknown',model_selector='unknown',reasoning_selector='unknown'))
for a in [C['source'],C['evaluation'],*C['responses'].values(),*load(PACK/'manifest.json')['artifacts']]:assert ref(ROOT/a['path'])==a
reply='zatwierdzam i kontynuuj'
save(M/'approval-evidence.json',dict(owner_reply_verbatim=reply,recorded_at_utc=now,owner_message_sent_at_utc='unknown',actual_owner_file_open_or_read='unknown',
    interpretation='Explicit assent to immediately presented .4c1 locator assessments and continuation to assigned .4c2. Acceptance of38 readable quotes and6 incomplete crops retains all44 strict envelope failures; no old meaning variants or locator repair.',
    presented_decisions=pres['decisions'],basis=[ref(PACK/'owner-focus.md'),ref(PACK/'presentation.json'),ref(PACK/'issues.json')],
    count_policy='44 distinct occurrence judgments. Geometry/strict envelopes and38+6 raster outcomes are facets of the same44, not88 or132 new judgments.'))
reviewer='owner in this chat; personal identity unknown';scopes=[]
for i,row in enumerate(packet['locators']):
    j=dict(id=row['id'],source_scope=row['source_scope'],source_quote_original=row['source_quote_original'],independent_source_helper=row['independent_source_helper'],source_image=row['source_image'],
        diagnostic_artifact=row['diagnostic_artifact'],diagnostic_pointer=row['diagnostic_pointer'],manual_assessment=row['manual_assessment'],evaluator_comparison=row['manual_comparison'],
        status='reviewed',reviewer=reviewer,recorded_at_utc=now,accepted_facets=dict(valid_geometry=True,quote_supported_on_full_source=True,strict_whole_glyph_containment=False,
            raster_result=row['raster_short_quote']),whole_evidence_record_accepted=False,original_locator_repaired=False,exclusions=row['exclusions'],uncertainties=row['uncertainties'],runs={})
    for run,x in row['runs'].items():
        j['runs'][run]=dict(response=C['responses'][run],reviewer=reviewer,status='reviewed',result='owner_accepted_bounded_locator_assessment',
            comparison_artifact=ref(PACK/'comparisons.json'),comparison_pointer=f'/locators/{i}/runs/{run}',output_trace=copy.deepcopy(x['output_trace']),
            geometry=x['geometry'],quote_location=x['quote_location'],raster_review=x['raster_review'],comparison=x['comparison'],
            inherited_report_observations=x['inherited_report_observations'],exclusions=x['exclusions'],original_locator_repaired=False,whole_record_accepted=False)
    scopes.append(j)
decision=dict(id='M-POC5A-owner-decision-08',card='M-POC5A',part='M-POC5A.4c1',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,reviewer=reviewer,owner_reply_verbatim=reply,
    decision='accepted_presented_locator_assessments_44_distinct_occurrences_geometry_and38readable_plus6incomplete',approval_evidence=ref(M/'approval-evidence.json'),
    prior_decision=ref(R/'owner-decision-07.json'),prior_state=ref(R/'current-state-16.json'),comparison_manifest=ref(PACK/'manifest.json'),focused_packet=ref(PACK/'owner-focus.md'),
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],recommendations=pres['decisions'],scopes=scopes,newly_reviewed_locator_occurrences=44,
    per_answer={'first-001':22,'context-01':22},valid_geometry=44,strict_quote_glyph_envelope_passes=0,strict_quote_glyph_envelope_failures=44,
    readable_raster_without_observed_ink_loss=38,readable_with_descenders_clipped=4,missing_final_quote_line=2,
    issue_disposition={'SEM-005':'Owner confirmed exact E916 locator defect in both answers; original rectangle not repaired, semantic variants not decided.',
        'SEM-007':'Owner accepted first22ID/44 locator assessments only;38 readable rasters+4descender clipping+2missing line, strict envelopes44fail. Remaining80 assigned occurrences and wider locator scope still pending.'},
    unresolved_prior_issue_ids=prior['unresolved_issue_ids'],pending_expectation_ids=prior['pending_expectation_ids'],
    count_policy='44 owner-reviewed locator occurrences with mixed facets; not44 good locators, rule TP or whole accepted records.',owner_file_open_or_read='unknown',metrics='not_assessable',
    excluded=pres['excludes'],no_response_changes=True,no_gold_change=True,no_new_sources=True,whole_card_closed=False)
save(R/'owner-decision-08.json',decision);dr=ref(R/'owner-decision-08.json');old=load(R/'owner-review-overlay-07.json');overlay=copy.deepcopy(old)
overlay.update(id='M-POC5A-owner-review-overlay-08',decision=dr,prior_overlay=ref(R/'owner-review-overlay-07.json'),locator_owner_decision=dr,
    owner_reviewed_locator_scoped_occurrences=44,all_locator_review='44 assigned locator occurrences reviewed in bounded mixed facets;80 assigned still unreviewed; full locator coverage not certified.',
    locator_count_policy=decision['count_policy'],pending_prior_issue_ids=prior['unresolved_issue_ids'])
overlay['issue_dispositions'].update(decision['issue_disposition'])
for run,v in overlay['runs'].items():
    v['locator_scopes']=[dict({k:z for k,z in j.items() if k!='runs'},response=C['responses'][run],decision=dr,trace=j['runs'][run]) for j in scopes]
    v['owner_reviewed_locator_scoped_occurrences']=22;v['assigned_remaining_unreviewed_locator_occurrences']=37 if run=='first-001' else 43
save(R/'owner-review-overlay-08.json',overlay)
state=copy.deepcopy(prior);state.update(id='M-POC5A-current-state-17',part='M-POC5A.4c1-owner-review',previous_state=ref(R/'current-state-16.json'),decision=dr,overlay=ref(R/'owner-review-overlay-08.json'),
    relationship_owner_decision=ref(R/'owner-decision-07.json'),locator_owner_decision=dr,new_owner_decisions=[dr],part_4c1_owner_review_complete=True,locator_owner_pending_compared_occurrences=0,
    locator_owner_reviewed_occurrences=44,all_locator_review_pending=False,next_part='M-POC5A.4c2',
    next_action='Execute assigned .4c2,21IDs/42occurrences after recorded60–80min estimate. Prior8expectations/older pending unchanged; no locator repair.',
    resume='Owner explicitly accepted .4c1 mixed locator facets44occurrences; strict44fail preserved,38readable+4clipped+2missing. SEM-005 defect assessment confirmed only, SEM-007 partial, both original defects and older meaning pending retained. Next.4c2.')
state['issue_dispositions'].update(decision['issue_disposition']);state['summary'].update(new_owner_reviewed_occurrences=44,owner_pending_occurrences=0,owner_accepted_scoped_occurrences=44)
save(R/'current-state-17.json',state)
(R/'owner-review-summary-08.md').write_text('''# Zatwierdzenie ocen lokatorów .4c1

Właściciel odpowiedział „zatwierdzam i kontynuuj”. Zapisano44 rozłączne
oceny wystąpień, osobno22 w każdej odpowiedzi. Zgoda obejmuje poprawną
geometrię i znalezienie cytatu w pełnym źródle,38 czytelnych krótkich
rastrów oraz6 niepełnych:4 z przyciętymi descenderami i2 z brakującą linią.
Wszystkie44 naruszenia pełnych obwiedni glifów zachowano; to nie44 dobre
lokatory ani44 poprawne reguły. Części decyzji nie dodają dodatkowych punktów.

SEM-005: potwierdzono wadęE916, bez naprawy lub rozstrzygnięcia semantyki.
SEM-007: przyjęto tylko pokazane44 oceny;80 następnych i szersza kompletność
pozostają otwarte. Oryginały/raporty/źródła/gold bez zmiany. Starsze pending,
8 oczekiwań,257 komponentowych decyzji relacji i264 pary rubryka/EXP zachowano.
Faktyczny odczyt plików unknown, pełne metryki nieocenialne.

Następna .4c2:21ID/42wystąpienia po oszacowaniu; .4c3/.4d osobno.
''',encoding='utf-8')
save(M/'owner-decision-artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-08.json','owner-review-overlay-08.json','current-state-17.json','owner-review-summary-08.md']]))
# Read current required inputs, including the newly leading additive decision.
paths=[ROOT/x['path'] for x in load(P/'measurement/M-POC5A-semantic-04c1/read-inputs.json')['files']]
paths += [R/'current-state-16.json',R/'current-state-17.json',R/'owner-decision-08.json',R/'owner-review-overlay-08.json',D/'handoff/2026-10-11-M-POC5A-semantic-04c1.md',D/'work/tasks/semantic/M-POC5A.4c2.md',planpath]
paths=list(dict.fromkeys(paths))
for p in paths:
    b=p.read_bytes();json.loads(b) if p.suffix=='.json' else b.decode('utf-8-sig')
save(M/'read-inputs.json',dict(files=[ref(p) for p in paths],method='Full required bytes read/JSON parsed; individual quote/glyph visual review separately recorded. Not semantic acceptance.'))
save(M/'scope-plan-reference.json',dict(artifact=ref(planpath),assigned_part=assigned,before_semantic_review=True))
public=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4c','.4c1','.4c2']]]
save(M/'public-documents-before.json',[ref(p) for p in public])
print(json.dumps(dict(new_owner_locator_scopes=44,prior_relation_scopes=257,assigned_next=42,protected=len(protected))))
