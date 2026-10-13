"""Record exact locator assent and estimate next assigned part before review."""
from pathlib import Path
from datetime import datetime,timezone
import copy,json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent;R=P/'reviews/semantic-01';PACK=R/'part-04c2';D=ROOT/'docs'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();C=load(R/'checklist.json');prior=load(R/'current-state-18.json');packet=load(PACK/'comparisons.json');pres=load(PACK/'presentation.json')
planpath=P/'measurement/M-POC5A-semantic-04c1/scope-plan.json';plan=load(planpath);assigned=plan['parts'][2];assert assigned['occurrences']==38
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(card='M-POC5A.4c3',recorded_at_utc=now,protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),prior_state=ref(R/'current-state-18.json'),
    estimate_before_locator_review=dict(minutes_range=[60,85],assigned_ids=22,assigned_occurrences=38,further_split_required=False,includes_recording_previous_bounded_assent=True),
    scope_plan=ref(planpath),active_time='unknown',model_selector='unknown',reasoning_selector='unknown'))
for a in [C['source'],C['evaluation'],*C['responses'].values(),*load(PACK/'manifest.json')['artifacts']]:assert ref(ROOT/a['path'])==a
reply='zatwierdzam i kontynuuj - powiedz ile jeszcze do końca etapu 5 ??'
save(M/'approval-evidence.json',dict(owner_reply_verbatim=reply,recorded_at_utc=now,owner_message_sent_at_utc='unknown',actual_owner_file_open_or_read='unknown',
    interpretation='Explicit assent to the immediately presented .4c2 recommendations:42 readable short quotes/geometry/source,40 measurable envelope failures,2 E962 numericprecision unresolved. Continue.4c3; request remainingstage5 work, no old meaning decisions.',
    presented_decisions=pres['decisions'],basis=[ref(PACK/'owner-focus.md'),ref(PACK/'presentation.json'),ref(PACK/'issues.json')],
    count_policy='42 distinct occurrence judgments;42+40+2 are overlapping facets of the same42.'))
reviewer='owner in this chat; personal identity unknown';scopes=[]
for i,row in enumerate(packet['locators']):
    j=dict(id=row['id'],source_scope=row['source_scope'],source_quote_original=row['source_quote_original'],independent_source_helper=row['independent_source_helper'],source_image=row['source_image'],
        diagnostic_artifact=row['diagnostic_artifact'],diagnostic_pointer=row['diagnostic_pointer'],manual_assessment=row['manual_assessment'],evaluator_comparison=row['manual_comparison'],
        status='reviewed',reviewer=reviewer,recorded_at_utc=now,accepted_facets=dict(valid_geometry=True,quote_supported_on_full_source=True,strict_whole_glyph_containment=row['strict_full_quote_glyph_envelope'],
            raster_result=row['raster_short_quote']),whole_evidence_record_accepted=False,original_locator_repaired=False,exclusions=row['exclusions'],uncertainties=row['uncertainties'],runs={})
    for run,x in row['runs'].items():
        j['runs'][run]=dict(response=C['responses'][run],reviewer=reviewer,status='reviewed',result='owner_accepted_bounded_locator_assessment',
            comparison_artifact=ref(PACK/'comparisons.json'),comparison_pointer=f'/locators/{i}/runs/{run}',output_trace=copy.deepcopy(x['output_trace']),
            geometry=x['geometry'],quote_location=x['quote_location'],raster_review=x['raster_review'],comparison=x['comparison'],
            inherited_report_observations=x['inherited_report_observations'],exclusions=x['exclusions'],original_locator_repaired=False,whole_record_accepted=False)
    scopes.append(j)
decision=dict(id='M-POC5A-owner-decision-09',card='M-POC5A',part='M-POC5A.4c2',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,reviewer=reviewer,owner_reply_verbatim=reply,
    decision='accepted_presented_locator_assessments42_geometry_readability_and40envelope_failures_plus2numericprecision',approval_evidence=ref(M/'approval-evidence.json'),
    prior_decision=ref(R/'owner-decision-08.json'),prior_state=ref(R/'current-state-18.json'),comparison_manifest=ref(PACK/'manifest.json'),focused_packet=ref(PACK/'owner-focus.md'),
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],recommendations=pres['decisions'],scopes=scopes,newly_reviewed_locator_occurrences=42,
    per_answer={'first-001':21,'context-01':21},valid_geometry=42,strict_quote_glyph_envelope_passes=0,strict_quote_glyph_envelope_failures=40,strict_quote_glyph_envelope_numericprecision_unresolved=2,raw_no_tolerance_envelope_false_occurrences=42,
    readable_raster_without_observed_ink_loss=42,readable_with_descenders_clipped=0,missing_final_quote_line=0,
    issue_disposition={'SEM-007':'Owner accepted86/124 assigned short-quote locator assessments: previous44 plus new42. New42 readable,40 distinguishable envelope failures,2E962 numericprecision unresolved. Remaining38 and broader content unreviewed; no locator repair or meaning closure.'},
    unresolved_prior_issue_ids=prior['unresolved_issue_ids'],pending_expectation_ids=prior['pending_expectation_ids'],
    count_policy='42 new owner-reviewed locator occurrences with mixed facets; not42 good locators, rule TP or whole accepted records.',owner_file_open_or_read='unknown',metrics='not_assessable',
    excluded=pres['excludes'],no_response_changes=True,no_gold_change=True,no_new_sources=True,whole_card_closed=False)
save(R/'owner-decision-09.json',decision);dr=ref(R/'owner-decision-09.json');old=load(R/'owner-review-overlay-08.json');overlay=copy.deepcopy(old)
overlay.update(id='M-POC5A-owner-review-overlay-09',decision=dr,prior_overlay=ref(R/'owner-review-overlay-08.json'),locator_owner_decision=dr,
    owner_reviewed_locator_scoped_occurrences=86,all_locator_review='86 assigned occurrences reviewed in bounded mixed facets;38 assigned still unreviewed; full coverage not certified.',
    locator_count_policy=decision['count_policy'],pending_prior_issue_ids=prior['unresolved_issue_ids'])
overlay['issue_dispositions'].update(decision['issue_disposition'])
for run,v in overlay['runs'].items():
    v['locator_scopes'] += [dict({k:z for k,z in j.items() if k!='runs'},response=C['responses'][run],decision=dr,trace=j['runs'][run]) for j in scopes]
    v['owner_reviewed_locator_scoped_occurrences']=43;v['assigned_remaining_unreviewed_locator_occurrences']=16 if run=='first-001' else 22
save(R/'owner-review-overlay-09.json',overlay)
state=copy.deepcopy(prior);state.update(id='M-POC5A-current-state-19',part='M-POC5A.4c2-owner-review',previous_state=ref(R/'current-state-18.json'),decision=dr,overlay=ref(R/'owner-review-overlay-09.json'),
    relationship_owner_decision=ref(R/'owner-decision-07.json'),locator_owner_decision=dr,new_owner_decisions=[dr],part_4c2_owner_review_complete=True,locator_owner_pending_compared_occurrences=0,
    locator_owner_reviewed_occurrences=86,all_locator_review_pending=False,next_part='M-POC5A.4c3',
    next_action='Execute assigned.4c3,22ID/38occurrences after recorded60–85min estimate. Then.4d scope before review and separateM-POC5B20situations. Older8expectations/meaning pending preserved.',
    resume='Explicit.4c2 assent42 facets recorded; owner total86. Strict40fail+2numericprecision unchanged. Next.4c3 only; remainingstage5 after that.4d and20situations, further sessions unknown until scope estimate.')
state['issue_dispositions'].update(decision['issue_disposition']);state['summary'].update(new_owner_reviewed_occurrences=42,owner_pending_occurrences=0,owner_accepted_scoped_occurrences=42)
save(R/'current-state-19.json',state)
(R/'owner-review-summary-09.md').write_text("# Zatwierdzenie .4c2\n\nWłaściciel: „"+reply+"”. Przyjęto42 ograniczone oceny: poprawne geometrie/źródłowe krótkie cytaty i czytelne rastry;40 mierzalnych ograniczeń pełnych obwiedni oraz2E962 tylko niepewność precyzji. To42 rozłączne wystąpienia, nie84 punkty lub dobre całe rekordy. Oryginały bez naprawy. Łącznie86 lokatorów z decyzjami,38 jeszcze nieprzejrzanych. Poprzednie257 ocen komponentów relacji/264 pary rubryka/EXP i8 oczekiwań oraz dawne SEM pozostają w swoim zakresie. Następna.4c3, potem.4d iM-POC5B20sytuacji; liczba dalszych sesji dopiero po oszacowaniu zakresu.\n",encoding='utf-8')
save(M/'owner-decision-artifacts.json',dict(artifacts=[ref(R/f) for f in ['owner-decision-09.json','owner-review-overlay-09.json','current-state-19.json','owner-review-summary-09.md']]))
# Read current required inputs, including the newly leading additive decision.
paths=[ROOT/x['path'] for x in load(P/'measurement/M-POC5A-semantic-04c2/read-inputs.json')['files']]
paths += [R/'current-state-18.json',R/'current-state-19.json',R/'owner-decision-09.json',R/'owner-review-overlay-09.json',D/'handoff/2026-10-11-M-POC5A-semantic-04c2.md',D/'work/tasks/semantic/M-POC5A.4c3.md',planpath]
paths=list(dict.fromkeys(paths))
for p in paths:
    b=p.read_bytes();json.loads(b) if p.suffix=='.json' else b.decode('utf-8-sig')
save(M/'read-inputs.json',dict(files=[ref(p) for p in paths],method='Full required bytes read/JSON parsed; individual quote/glyph visual review separately recorded. Not semantic acceptance.'))
save(M/'scope-plan-reference.json',dict(artifact=ref(planpath),assigned_part=assigned,before_semantic_review=True))
public=[D/'STATUS.md',D/'ROADMAP.md',D/'HANDOFF.md',D/'work/tasks/M-POC5A.md',*[D/f'work/tasks/semantic/M-POC5A{x}.md' for x in ['.4','.4c','.4c2','.4c3']]]
save(M/'public-documents-before.json',[ref(p) for p in public])
print(json.dumps(dict(new_owner_locator_scopes=42,prior_relation_scopes=257,assigned_next=38,protected=len(protected))))
