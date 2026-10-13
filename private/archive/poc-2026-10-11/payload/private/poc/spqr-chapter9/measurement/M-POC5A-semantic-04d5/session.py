import json,pathlib,hashlib,datetime,sys,copy,collections
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9';R=P/'reviews/semantic-01';M=pathlib.Path(__file__).parent
def read(f):return json.loads(f.read_text(encoding='utf-8-sig'))
def ref(f):
    b=f.read_bytes();return dict(path=f.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(f,o):f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def md(f,s):f.write_text(s.rstrip()+'\n',encoding='utf-8')
def pointer(o,p):
    for k in p.strip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');o=o[int(k)] if isinstance(o,list) else o[k]
    return o
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()

def init():
    assert ROOT.as_posix()=='C:/repo/wargame-compiler'
    anchors=read(P/'measurement/M-POC5A-semantic-04d4/preflight.json')['verified']
    for a in anchors:assert ref(ROOT/a['path'])==a
    save(M/'preflight.json',dict(recorded_at_utc=now(),verified=anchors,all_match=True))
    save(M/'immutability-before.json',dict(files=[ref(f) for f in P.rglob('*') if f.is_file() and M not in f.parents],sessions_prefix_only=True))
    scope=read(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json')['parts'][4]
    save(M/'estimate.json',dict(recorded_at_utc=now(),before_reconciliation=True,card='M-POC5A.4d5',minutes_range=[65,85],limit_minutes=90,
      assignment=scope,scope_plan=ref(P/'measurement/M-POC5A-semantic-04d1/scope-plan.json'),scope_pointer='/parts/4',
      rationale='Reconcile exact prior decisions against all207 inventory IDs,74 expectation scopes,277 category pairs and old issues; inspect excluded fields/old pending for boundaries, without assigning new rule points or re-deciding old variants.',
      other_cards_executed=[],M_POC5B_estimate='not_yet_prepared',active_time='unknown'))
    print('Five anchors verified; fresh65–85minute .4d5 estimate recorded before work.')

def approve():
    old=read(R/'current-state-28.json');packet=read(R/'part-04d4/comparisons.json');pres=read(R/'part-04d4/presentation.json')
    for a in read(R/'part-04d4/manifest.json')['artifacts']:assert ref(ROOT/a['path'])==a
    evidence=dict(owner_reply_verbatim='zatwierdzam i kontynuuj',message_sent_at_utc='unknown',recorded_at_utc=now(),
      preceding_presentation=ref(R/'part-04d4/presentation.json'),focused_packet=ref(R/'part-04d4/owner-focus.md'),
      preceding_offer='Accept80 bounded supported judgments and2mixed C-9.95-02 judgments, confirming SEM-022 limited omission; preserve8old pending/13old issues.',
      interpretation='Approval applies to both numbered recommendations in immediately preceding final reply. Continue authorizes next .4d5; no old unresolved variant selected.',
      followup_question_verbatim='ile do końca POC5 ?',owner_file_open_or_read='unknown')
    save(M/'approval-evidence.json',evidence)
    assert not (R/'owner-decision-14.json').exists()
    scopes=copy.deepcopy(packet['inventory'])
    for x in scopes:
        for run,r in x['runs'].items():
            r.update(status='reviewed',human_reviewer='owner in this chat; personal identity unknown',owner_decision='accepted_presented_bounded_judgment')
    decision=dict(id='M-POC5A-owner-decision-14',card='M-POC5A',part='M-POC5A.4d4',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now(),
      reviewer='owner in this chat; personal identity unknown',owner_reply_verbatim=evidence['owner_reply_verbatim'],decision='accepted_all82_presented_bounded_inventory_judgments',
      approval_evidence=ref(M/'approval-evidence.json'),prior_decision=old['decision'],prior_state=ref(R/'current-state-28.json'),
      comparison_manifest=ref(R/'part-04d4/manifest.json'),focused_packet=ref(R/'part-04d4/owner-focus.md'),evaluation=old['evaluation'],responses=old['responses'],
      recommendations=[pres['positive_set'],pres['separate_decisions'][0]],scopes=scopes,newly_reviewed_inventory_occurrences=82,per_answer={'first-001':41,'context-01':41},
      bounded_supported_occurrences=80,mixed_clause_occurrences=2,underlying_omitted_explanatory_clauses_per_answer=1,
      issue_disposition='SEM-022 confirmed only as one omitted historical explanatory clause per answer in R995 textual content. Operative content/source image retained; no demonstrated wrong game result, automatic FN, new rule or response repair.',
      unresolved_prior_issue_ids=old['inherited_issue_ids'],pending_expectation_ids=old['pending_expectation_ids'],
      count_policy='82 exact inventory judgments, not82wholecorrectrecords. 80supported+2mixed. Prior332 inventory decisions retained; no new rubric points.',
      owner_file_open_or_read='unknown',metrics='not_assessable',no_response_changes=True,no_gold_change=True,no_new_sources=True,whole_card_closed=False)
    save(R/'owner-decision-14.json',decision)
    overlay=read(R/'owner-review-overlay-13.json')
    overlay.update(id='M-POC5A-owner-review-overlay-14',decision=ref(R/'owner-decision-14.json'),prior_overlay=ref(R/'owner-review-overlay-13.json'),
      inventory_owner_decision=ref(R/'owner-decision-14.json'),owner_reviewed_inventory_scoped_occurrences=414)
    overlay['issue_dispositions']['SEM-022']=decision['issue_disposition']
    for run,data in overlay['runs'].items():
        for x in scopes:
            data['inventory_scopes'].append(dict(id=x['id'],source_scopes=x['source_scopes'],manual_assessment=x['runs'][run]['bounded_result'],
               comparison=x['manual_comparison'],decision=ref(R/'owner-decision-14.json'),trace=x['runs'][run],status='reviewed',
               reviewer=decision['reviewer'],whole_record_accepted=False))
        data['owner_reviewed_inventory_scoped_occurrences']=207
        assert len(data['inventory_scopes'])==207 and len({x['id'] for x in data['inventory_scopes']})==207
    save(R/'owner-review-overlay-14.json',overlay)
    s=copy.deepcopy(old);s.update(id='M-POC5A-current-state-29',part='M-POC5A.4d4-owner-review',previous_state=ref(R/'current-state-28.json'),
      decision=ref(R/'owner-decision-14.json'),overlay=ref(R/'owner-review-overlay-14.json'),inventory_owner_decision=ref(R/'owner-decision-14.json'),
      inventory_owner_reviewed_assigned_occurrences=414,inventory_owner_reviewed_new_occurrences=82,inventory_owner_pending_compared_occurrences=0,
      part_4d4_owner_review_complete=True,all_assigned_inventory_owner_scoped_review_complete=True,
      current_part_owner_pending_issue_ids=[],unresolved_issue_ids=old['inherited_issue_ids'],new_owner_decisions=[ref(R/'owner-decision-14.json')],
      resume='Owner accepted82 bounded .4d4 judgments;414inventory scopes decided. Next .4d5 reconciliation; old8expectations/13issues retained.',
      next_action='Execute .4d5 reconciliation in its exact assigned scope after fresh estimate. M-POC5B remains separate.')
    s['summary'].update(new_owner_reviewed_occurrences=82,owner_pending_occurrences=0,owner_accepted_scoped_occurrences=82,owner_accepted_supported_occurrences=80,owner_decided_mixed_or_omission_occurrences=2)
    s['issue_dispositions']['SEM-022']=decision['issue_disposition'];s['inventory_comparison_counters'].update(owner_decided=414,owner_pending=0)
    save(R/'current-state-29.json',s)
    md(R/'owner-review-summary-14.md','''# Zatwierdzenie .4d4

Właściciel: „zatwierdzam i kontynuuj”. Przyjęto wszystkie82 przedstawione oceny:80 ograniczonych ocen wsparcia i2mieszane C-9.95-02. SEM-022 potwierdzono wyłącznie jako pominięcie jednego wyjaśnienia historycznego na odpowiedź w textual content; operatywna treść i źródłowy obraz zachowane. Bez wykazanego błędnego wyniku gry, automatycznego FN, nowej reguły lub naprawy.

Łącznie414 zakresów inwentarza ma decyzje,207 na odpowiedź. To nie414 całych poprawnych rekordów. Starsze8 oczekiwań/13 kwestii pozostają otwarte. Kontynuacja dotyczy .4d5, potem osobno M-POC5B40 ocen sytuacji.
''')
    print('Owner-decision/overlay14 and current-state29 saved;414 scopes decided, old8/13 retained.')

def show_pending(wanted):
    parts=[read(R/f'{part}/comparisons.json') for part in ['part-02','part-03','part-04a']]
    cases={x['id']:x for part in parts for x in part['expectations']}
    for id in wanted:
        x=cases[id];print('\n',id,'SCOPE',x['source_scope'],'EXCLUDED',x['unreviewed_fields'],'LIMITS',x['limits'])
        for e in x['source_evidence']:
            print('SOURCE',e.get('source_span'),e.get('source_transcription',e.get('transcription','graphic; supplied source image')))
        for run,d in x['runs'].items():
            print('ANSWER',run,'COMPARISON',d['comparison'])
            for oid,tr in d['output_trace'].items():
                v=tr['original_record'];print(oid,tr['pointer'],tr['raw_span'])
                print(json.dumps({k:val.get('value',val) if isinstance(val,dict) else val for k,val in v.items()
                  if k in ['transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','content','blocking','reason','needed_context','gap_ids']},ensure_ascii=False))
            print('GAP CLAIMS',json.dumps(d.get('gap_claims',[]),ensure_ascii=False)[:4500])

if __name__=='__main__':
    if sys.argv[1]=='init':init()
    elif sys.argv[1]=='approve':approve()
    elif sys.argv[1]=='pending':show_pending(sys.argv[2:])
