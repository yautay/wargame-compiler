"""Record the real owner's bounded acceptance; preserve all prior evidence and pending choices."""
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
for tree in ['source','runs','proposals','reports','inputs','context','transfer','evaluation/eval-v1',
             'reviews','measurement/M-POC5A-semantic-01','measurement/M-POC5A-semantic-02']:
    protected += [ref(f) for f in sorted((P/tree).rglob('*')) if f.is_file()]
save(M/'start.json',dict(card='M-POC5A',part='M-POC5A.2-owner-review',
    first_recorded_clock_utc='2026-10-10T19:02:15+00:00',bootstrap_start='unknown',
    protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),owner_message='akceptuję',
    owner_message_sent_at_utc='unknown',first_recorded_clock_after_owner_message=True))

C=load(REV/'checklist.json')
D=load(REV/'part-02/comparisons.json')
for r in list(C['responses'].values())+[C['evaluation'],C['source']]:assert ref(ROOT/r['path'])==r
manifest=load(REV/'part-02/manifest.json')
for r in manifest['artifacts']:assert ref(ROOT/r['path'])==r
accepted=[e for e in D['expectations'] if e['proposed_assessment'] in ['supported_local_scope','supported_local_scope_with_locator_issue']]
ids={e['id'] for e in accepted}
expected={f'EXP-{n:03}' for n in list(range(1,10))+list(range(11,17))+[18]+list(range(20,26))}
assert ids==expected and len(accepted)==22
assert all(e['classification']=='confirmed_local_content_scope' for e in accepted)
now=datetime.now(timezone.utc).isoformat()
reviewer='owner in this chat; personal identity unknown'
scope_rows=[]
for e in accepted:
    scope_rows.append(dict(id=e['id'],reviewed_scope=e['source_scope'],source_evidence=e['source_evidence'],
        inventory_refs=e['inventory_refs'],criticality=e['criticality'],status='reviewed',
        result='correct_in_owner_accepted_scope',reviewer=reviewer,recorded_at_utc=now,
        evidence_comparison=e['comparison'],limits=e['limits'],unreviewed_fields=e['unreviewed_fields'],
        output_trace={run:{rid:dict(pointer=t['pointer'],raw_span=t['raw_span']) for rid,t in r['output_trace'].items()}
            for run,r in e['runs'].items()},
        locator_status='E916 confirmed failure preserved' if e['id']=='EXP-016' else 'no new locator approval',
        whole_record_accepted=False))

decision=dict(id='M-POC5A-owner-decision-01',card='M-POC5A',part='M-POC5A.2',date='2026-10-10',
    timezone='Europe/Warsaw',recorded_at_utc=now,owner_message_sent_at_utc='unknown',reviewer=reviewer,
    owner_reply='akceptuję',decision='accepted_exact_22_local_scopes_in_both_answers',
    interpretation_basis='Owner accepted after the last explicit offer of 22 correct local scopes. EXP-010/017/019 were excluded from that offer. SEM-009 had mutually different choices; this reply does not choose one.',
    evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
    presentation=ref(REV/'part-02/presentation.json'),focused_packet=ref(REV/'part-02/owner-focus.md'),
    comparison_manifest=ref(REV/'part-02/manifest.json'),scopes=scope_rows,
    accepted_group_count_per_answer=22,
    exclusions=['EXP-010 source-block judgment','EXP-017/SEM-001 unresolved local branch',
        'EXP-019/SEM-009 alternative blocking choices','previous SEM-002/003 decisions',
        'E916 locator and all glyph boundaries','full inventory records outside accepted spans',
        'all relations and TP/FP/FN','unreviewed metadata, alias/target identities and graphic ratings',
        'full external procedures or real setup','20 situation outcomes','full graph/depth/time-budget compliance'],
    owner_opened_report_or_images='unknown',semantic_acceptance='bounded_owner_acceptance_only',
    M_POC5A_closed=False,corrections=0,new_extractions=0)
save(REV/'owner-decision-01.json',decision)
decision_ref=ref(REV/'owner-decision-01.json')

category_rows=[]
for r in C['category_units']:
    unit=r['frozen_unit']
    if unit['expectation_id'] not in ids:continue
    category_rows.append(dict(id=r['id'],category=r['category'],expectation_id=unit['expectation_id'],
        scoped_content=unit['scoped_content'],status='reviewed',result='correct_in_owner_accepted_scope',
        reviewer=reviewer,decision=decision_ref,
        derivation='Relevant components of the fully accepted reviewed_scope only; not a separate rule point or whole-category acceptance.',
        original_unit=unit))
assert len(category_rows)==85
counts=Counter(r['category'] for r in category_rows)
all_ids=[e['id'] for e in C['expectations']]
pending=[i for i in all_ids if i not in ids]
assert len(pending)==52
reviewed_runs={}
for run,response in C['responses'].items():
    reviewed_runs[run]=dict(response=response,evaluation=C['evaluation'],
        scopes=[dict(r,response=response,decision=decision_ref) for r in scope_rows],
        content_group_denominator=66,accepted_scoped_groups=22,pending_content_groups=44,
        context_group_denominator=8,reviewed_context_groups=0,pending_context_groups=8,
        complete_rule_quality='not_assessable',semantic_TP_FP_FN='not_assessable')
overlay=dict(id='M-POC5A-owner-review-overlay-01',decision=decision_ref,evaluation=C['evaluation'],
    base_checklist=ref(REV/'checklist.json'),comparison_packet=ref(REV/'part-02/manifest.json'),
    responses=C['responses'],runs=reviewed_runs,category_units=category_rows,
    category_accepted_scope_counts=dict(counts),category_full_denominators=C['counts']['categories'],
    inventory_scope_policy='Only accepted EXP-owned source spans in their inventory_refs; do not mark whole 42 mapped items or whole parents accepted.',
    pending_expectation_ids=pending,pending_prior_issue_ids=['SEM-001','SEM-002','SEM-003','SEM-004','SEM-005','SEM-006','SEM-007','SEM-008','SEM-009'],
    all_output_edges_review='pending',all_locator_review='unchanged',full_semantic_metrics='not_assessable',
    no_new_gold=True,no_response_changes=True,no_situation_review=True)
save(REV/'owner-review-overlay-01.json',overlay)
current=dict(id='M-POC5A-current-state-03',card='M-POC5A',part='M-POC5A.2',status='partial_waiting_review',
    previous_state=ref(REV/'current-state-02.json'),decision=decision_ref,overlay=ref(REV/'owner-review-overlay-01.json'),
    evaluation=C['evaluation'],responses=C['responses'],owner_reviewed_local_groups_per_answer=22,
    remaining_pending_expectations=52,pending_in_part_02=['EXP-010','EXP-017','EXP-019'],
    remaining_uncompared_expectations=49,full_metrics='not_assessable',
    semantic_acceptance='bounded_22_local_scopes_in_both_answers',M_POC5A_closed=False,
    resume='Clarify SEM-009 alternative; remaining pending SEM-001/002/003, EXP-010 and next separate .3/.4 scope. No extraction or correction.')
save(REV/'current-state-03.json',current)
text='''# Decyzja właściciela — 22 lokalne zakresy obu wyników

Właściciel odpowiedział „akceptuję” po przedstawieniu pakietu 22 zgodnych
lokalnych zakresów. Zapis: [owner-decision-01.json](owner-decision-01.json),
osobne oceny obu hashów: [owner-review-overlay-01.json](owner-review-overlay-01.json).
Aktualny wskaźnik: [current-state-03.json](current-state-03.json).

Akceptacja: EXP-001–009, EXP-011–016, EXP-018, EXP-020–025, tylko dokładny
reviewed_scope na niezmienionym eval-v1, w first-001 i context-01.
Akceptacja EXP-016 dotyczy znaczenia; dawny błąd lokatora E916 zachowany.
Nie poświadczono otwarcia konkretnych plików/obrazów przez właściciela.

Po 22/66 potwierdzonych lokalnych zakresów; 44 lokalne i 8 kontekstu nadal
pending. To pokrycie przeglądu, nie pełny procent jakości. 85 diagnostycznych
par rubryka/EXP dziedziczy zgodność wyłącznie potwierdzonych komponentów;
nie stanowi 85 dodatkowych punktów reguł ani akceptacji całych kategorii.
Całe pozycje inwentarza, małe wartości grafik, aliasy, krawędzie i lokatory
nie są automatycznie zaakceptowane.

EXP-010, EXP-017/SEM-001 i EXP-019/SEM-009 nie były objęte listą 22.
SEM-009 miało dwa rozbieżne warianty; „akceptuję” nie wskazuje wyboru.
Wcześniejsze SEM-002/003 również pozostają pending. Pozostałe 49 oczekiwań
ma osobne zakresy części .3/.4. M-POC5A nadal partial/waiting_review.
Nie oceniono sytuacji i nie nadano TP/FP/FN, pełnej jakości lub zgodności czasu.
Źródeł, odpowiedzi, zamrożonej oceny i wcześniejszych raportów nie zmieniono.
'''
path=REV/'owner-review-summary-01.md';assert not path.exists();path.write_text(text,encoding='utf-8')
save(M/'decision-artifacts.json',dict(artifacts=[ref(REV/f) for f in ['owner-decision-01.json','owner-review-overlay-01.json','current-state-03.json','owner-review-summary-01.md']],
    semantic_acceptance='actual_owner_decision_in_exact_scope',owner_reply='akceptuję'))
print(json.dumps(dict(owner_accepted_groups_per_answer=22,pending_expectations=52,
    scoped_category_units=85,category_counts=dict(counts),protected_files=len(protected),
    SEM_009='pending_alternative_choice',whole_card='partial_waiting_review'),ensure_ascii=False))
