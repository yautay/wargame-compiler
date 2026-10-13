"""Record the owner's part-03 acceptance and produce a cumulative additive review state."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01'
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(path,obj):
    assert not path.exists(),path
    path.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
protected=[]
for tree in ['source','runs','proposals','reports','inputs','context','transfer','evaluation/eval-v1','reviews',
             'measurement/M-POC5A-semantic-01','measurement/M-POC5A-semantic-02','measurement/M-POC5A-semantic-03',
             'measurement/M-POC5A-owner-review-001']:
    protected += [ref(f) for f in sorted((P/tree).rglob('*')) if f.is_file()]
reply='Akceptuję i podaj prompt dla nowej sesji'
save(M/'start.json',dict(card='M-POC5A',part='M-POC5A.3-owner-review',
    first_recorded_clock_utc='2026-10-10T19:56:27+00:00',bootstrap_start='unknown',protected=protected,
    sessions_before=ref(P/'measurement/sessions.jsonl'),owner_reply=reply,owner_message_sent_at_utc='unknown'))
C=load(REV/'checklist.json');D=load(REV/'part-03/comparisons.json')
old=load(REV/'owner-review-overlay-01.json')
for r in list(C['responses'].values())+[C['evaluation'],C['source']]:assert ref(ROOT/r['path'])==r
for r in load(REV/'part-03/manifest.json')['artifacts']:assert ref(ROOT/r['path'])==r
local=[e for e in D['expectations'] if e['proposed_assessment']=='supported_local_scope']
context=[e for e in D['expectations'] if e['proposed_assessment']=='source_block_supported']
local_ids={e['id'] for e in local};context_ids={e['id'] for e in context}
expected={f'EXP-{n:03}' for n in list(range(26,31))+[32]+list(range(34,40))+list(range(41,50))}
assert local_ids==expected and len(local)==21 and context_ids=={'EXP-031','EXP-033'}
now=datetime.now(timezone.utc).isoformat();reviewer='owner in this chat; personal identity unknown'
scopes=[]
for e in local+context:
    is_context=e['id'] in context_ids
    scopes.append(dict(id=e['id'],classification=e['classification'],reviewed_scope=e['source_scope'],
        source_evidence=e['source_evidence'],inventory_refs=e['inventory_refs'],criticality=e['criticality'],
        status='reviewed',result='correct_source_requirement_declaration' if is_context else 'correct_in_owner_accepted_scope',
        full_dependent_result='blocked_source' if is_context else 'outside_this_scoped_review',
        reviewer=reviewer,recorded_at_utc=now,evidence_comparison=e['comparison'],
        limits=e['limits'],unreviewed_fields=e['unreviewed_fields'],whole_record_accepted=False,
        output_trace={run:{rid:dict(pointer=t['pointer'],raw_span=t['raw_span']) for rid,t in r['output_trace'].items()}
            for run,r in e['runs'].items()}))
decision=dict(id='M-POC5A-owner-decision-02',card='M-POC5A',part='M-POC5A.3',date='2026-10-10',
    timezone='Europe/Warsaw',recorded_at_utc=now,owner_message_sent_at_utc='unknown',reviewer=reviewer,
    owner_reply=reply,decision='accepted_exact_21_local_scopes_and_2_source_requirements_in_both_answers',
    interpretation_basis='Latest offered positive set explicitly includes 21 local scopes and EXP-031/033 source needs. EXP-040/050 and alternative issue choices were excluded. Request for a prompt does not authorize creating a chat or publishing Git.',
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
    prior_decision=ref(REV/'owner-decision-01.json'),presentation=ref(REV/'part-03/presentation.json'),
    focused_packet=ref(REV/'part-03/owner-focus.md'),comparison_manifest=ref(REV/'part-03/manifest.json'),
    scopes=scopes,accepted_local_groups_this_decision_per_answer=21,
    reviewed_context_requirements_this_decision_per_answer=2,
    excluded=['EXP-040/SEM-002 per-unit interpretation','EXP-050/SEM-010 alternative setup declarations',
        'SEM-001 unresolved branch','SEM-009 alternative blocking choice',
        'SEM-003 new operator/exception acceptance, AS/LC order or final result',
        'E916 and all glyph boundaries','all relations and TP/FP/FN',
        'whole inventory records, metadata/aliases and tiny graphic ratings',
        'full real setup/external procedures','20 situation outcomes','full graph/depth/time-budget compliance'],
    context_acceptance_is_gap_closure=False,owner_opened_report_or_images='unknown',M_POC5A_closed=False,
    new_extractions=0,new_corrections=0)
save(REV/'owner-decision-02.json',decision);decision_ref=ref(REV/'owner-decision-02.json')
new_local_scopes=[r for r in scopes if r['id'] in local_ids]
context_scopes=[r for r in scopes if r['id'] in context_ids]
runs={}
for run,response in C['responses'].items():
    previous=old['runs'][run]['scopes']
    merged=previous+[dict(r,response=response,decision=decision_ref) for r in new_local_scopes]
    assert len(merged)==43 and len({r['id'] for r in merged})==43
    runs[run]=dict(response=response,evaluation=C['evaluation'],scopes=merged,
        context_requirements=[dict(r,response=response,decision=decision_ref) for r in context_scopes],
        content_group_denominator=66,accepted_scoped_groups=43,pending_content_groups=23,
        context_group_denominator=8,reviewed_context_groups=2,pending_context_groups=6,
        context_full_resolution='blocked_source; no declared gap closure',
        complete_rule_quality='not_assessable',semantic_TP_FP_FN='not_assessable')
new_categories=[]
for r in C['category_units']:
    u=r['frozen_unit']
    if u['expectation_id'] not in local_ids:continue
    new_categories.append(dict(id=r['id'],category=r['category'],expectation_id=u['expectation_id'],
        scoped_content=u['scoped_content'],status='reviewed',result='correct_in_owner_accepted_scope',
        reviewer=reviewer,decision=decision_ref,original_unit=u,
        derivation='Relevant components of the owner-accepted reviewed_scope; no extra rule point or full-category approval.'))
assert len(new_categories)==90
categories=old['category_units']+new_categories
assert len(categories)==175 and len({r['id'] for r in categories})==175
accepted_ids={r['id'] for r in runs['first-001']['scopes']}|context_ids
pending=[e['id'] for e in C['expectations'] if e['id'] not in accepted_ids]
assert len(pending)==29
overlay=dict(id='M-POC5A-owner-review-overlay-02',decision=decision_ref,prior_overlay=ref(REV/'owner-review-overlay-01.json'),
    evaluation=C['evaluation'],base_checklist=ref(REV/'checklist.json'),responses=C['responses'],runs=runs,
    category_units=categories,category_accepted_scope_counts=dict(Counter(r['category'] for r in categories)),
    category_full_denominators=C['counts']['categories'],pending_expectation_ids=pending,
    pending_prior_issue_ids=old['pending_prior_issue_ids']+['SEM-010'],
    inventory_scope_policy=old['inventory_scope_policy'],all_output_edges_review='pending',all_locator_review='unchanged',
    full_semantic_metrics='not_assessable',no_new_gold=True,no_response_changes=True,no_situation_review=True)
save(REV/'owner-review-overlay-02.json',overlay)
save(REV/'current-state-05.json',dict(id='M-POC5A-current-state-05',card='M-POC5A',next_part='M-POC5A.4a',
    status='partial_waiting_review',previous_state=ref(REV/'current-state-04.json'),decision=decision_ref,
    overlay=ref(REV/'owner-review-overlay-02.json'),evaluation=C['evaluation'],responses=C['responses'],
    owner_accepted_local_groups_per_answer=43,reviewed_context_requirements_per_answer=2,
    remaining_pending_expectations=29,pending_in_prior_parts=['EXP-010','EXP-017','EXP-019','EXP-040','EXP-050'],
    remaining_uncompared_expectations=24,context_requirements_still_block_full_results=True,
    all_relations_and_locators_pending=True,M_POC5A_closed=False,
    resume='New manually started session: M-POC5A.4a EXP-051–074 only. Follow the saved continuation prompt; residual prior issues remain pending, then separate graph/locator/reconciliation parts.'))
summary='''# Decyzja właściciela — przyjęcie części .3 i stan łączny

Właściciel: „Akceptuję i podaj prompt dla nowej sesji”.
Zapis: [owner-decision-02.json](owner-decision-02.json).
Łączny stan obu odpowiedzi: [owner-review-overlay-02.json](owner-review-overlay-02.json)
i [current-state-05.json](current-state-05.json).

Nowa akceptacja w obu hashach: EXP-026–030, EXP-032, EXP-034–039,
EXP-041–049 (21 lokalnych reviewed_scope) oraz potrzeby/blokady źródła
EXP-031 i EXP-033. Te dwa wymagania kontekstu nie zamykają pełnych wyników,
luk źródła, operatorów SEM-003, kolejności AS/LC lub sytuacji.

Łącznie w każdej odpowiedzi 43/66 lokalnych zakresów przyjętych i 2/8
wymagań kontekstu przejrzanych. 23 lokalne i 6 kontekstu nadal pending:
29 oczekiwań, w tym 5 wcześniejszych oraz ostatnie 24 EXP-051–074.
175 par rubryka/EXP dziedziczy tylko zgodność zaakceptowanych komponentów,
nie zwiększa mianownika reguł i nie stanowi akceptacji całych kategorii.

EXP-040/SEM-002, EXP-050/SEM-010 oraz SEM-001/003/009 nadal pending.
E916 i 64 granice glifów, wszystkie relacje, nieprzejrzane pola/aliasy,
małe ratingi grafik i realny setup wyłączone z akceptacji.
Nie poświadczono otwarcia konkretnych obrazów przez właściciela.
Pełna jakość i TP/FP/FN not_assessable; M-POC5A pozostaje partial.
Źródła, odpowiedzi, eval-v1, wcześniejsze review/raporty/pomiary zachowane.

Następna ręczna sesja: M-POC5A.4a, tylko EXP-051–074 i przypisane zakresy.
Pozostały inwentarz, graf, lokatory i rozliczenie będą osobnymi częściami.
'''
path=REV/'owner-review-summary-02.md';assert not path.exists();path.write_text(summary,encoding='utf-8')
save(M/'decision-artifacts.json',dict(artifacts=[ref(REV/f) for f in ['owner-decision-02.json','owner-review-overlay-02.json','current-state-05.json','owner-review-summary-02.md']],
    semantic_acceptance='actual_owner_exact_scope',owner_reply=reply))
print(json.dumps(dict(local_groups_per_answer=43,context_requirements_reviewed_per_answer=2,
    pending_expectations=29,category_units=175,protected_files=len(protected),next_part='M-POC5A.4a'),ensure_ascii=False))
