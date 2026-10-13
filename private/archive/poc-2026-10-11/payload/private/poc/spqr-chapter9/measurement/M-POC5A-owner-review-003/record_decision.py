"""Record the owner's bounded acceptance after the plain-language explanation."""
from pathlib import Path
from datetime import datetime, timezone
from collections import Counter
import hashlib,json,sys
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent;REV=P/'reviews/semantic-01'
sys.stdout.reconfigure(encoding='utf-8')
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
now=datetime.now(timezone.utc).isoformat();reply='zatwierdzzm'
protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
save(M/'start.json',dict(part='M-POC5A.4a-owner-review',recorded_at_utc=now,bootstrap_start='unknown',protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),owner_reply=reply,owner_message_sent_at_utc='unknown'))
save(M/'approval-evidence.json',dict(date='2026-10-11',timezone='Europe/Warsaw',owner_reply_verbatim=reply,owner_request_before_reply='ok żeby podjąć decyzję musisz mi to opisac po ludzku, z tego cco napisałeś niewiele rozumiem',last_offer_verbatim='Moja propozycja na teraz: przyjąć wskazane 20 zgodnych zakresów i poprawne wymaganie danych scenariusza, a te trzy przypadki pozostawić otwarte. To przyjęcie konkretnej części odpowiedzi; pełna poprawność obu wyników nadal wymaga dalszego przeglądu.',plain_language_explanation_summary=['Both saved answers compared to source; scoped review, not a game engine result.','20 local scopes retain reviewed conditions/numbers/exceptions/timing. EXP-064 correctly requires actual scenario BI leader/Initiative/membership; accepting the need does not supply those facts.','EXP-052 both Triarii gates separately present, conjunction not explicit; remain open.','EXP-066 local ignore instruction present but exact-table identification gap nonblocking; remain open.','EXP-074 illustrative rating boundary present but actual-value conditional block not explicit; remain open.'],interpretation='Direct human assent to the immediately preceding bounded offer. Preserve the verbatim typo; no choice for the three excluded cases.',owner_opened_files_or_images='unknown'))
C=load(REV/'checklist.json');D=load(REV/'part-04a/comparisons.json');old=load(REV/'owner-review-overlay-02.json')
for r in list(C['responses'].values())+[C['evaluation'],C['source']]:assert ref(ROOT/r['path'])==r
for r in load(REV/'part-04a/manifest.json')['artifacts']:assert ref(ROOT/r['path'])==r
local=[e for e in D['expectations'] if e['proposed_assessment']=='supported_local_scope']
context=[e for e in D['expectations'] if e['proposed_assessment']=='source_block_supported']
local_ids={e['id'] for e in local};context_ids={e['id'] for e in context}
assert len(local)==20 and local_ids=={f'EXP-{n:03}' for n in [51]+list(range(53,64))+[65]+list(range(67,74))}
assert context_ids=={'EXP-064'}
reviewer='owner in this chat; personal identity unknown';scopes=[]
for e in local+context:
    is_context=e['id'] in context_ids
    scopes.append(dict(id=e['id'],classification=e['classification'],reviewed_scope=e['source_scope'],source_evidence=e['source_evidence'],inventory_refs=e['inventory_refs'],criticality=e['criticality'],status='reviewed',result='correct_source_requirement_declaration' if is_context else 'correct_in_owner_accepted_scope',full_dependent_result='blocked_source' if is_context else 'outside_this_scoped_review',reviewer=reviewer,recorded_at_utc=now,evidence_comparison=e['comparison'],limits=e['limits'],unreviewed_fields=e['unreviewed_fields'],whole_record_accepted=False,primary_output_ids=e['primary_output_ids'],trace_policy='Evidence locators only. Acceptance applies to EXP-owned reviewed_scope components, not whole records/fields or supplemental context.',output_trace={run:{rid:dict(pointer=t['pointer'],raw_span=t['raw_span']) for rid,t in r['output_trace'].items()} for run,r in e['runs'].items()}))
decision=dict(id='M-POC5A-owner-decision-03',card='M-POC5A',part='M-POC5A.4a',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now,owner_message_sent_at_utc='unknown',reviewer=reviewer,owner_reply=reply,decision='accepted_exact_20_local_scopes_and_1_source_requirement_in_both_answers',interpretation_basis='Owner accepted the immediately preceding plain-language offer: 20 local scopes plus EXP-064 source need, with EXP-052/066/074 kept open.',approval_evidence=ref(M/'approval-evidence.json'),evaluation=C['evaluation'],responses=C['responses'],source=C['source'],prior_decision=ref(REV/'owner-decision-02.json'),presentation=ref(REV/'part-04a/presentation.json'),focused_packet=ref(REV/'part-04a/owner-focus.md'),comparison_manifest=ref(REV/'part-04a/manifest.json'),scopes=scopes,accepted_local_groups_this_decision_per_answer=20,reviewed_context_requirements_this_decision_per_answer=1,excluded=['EXP-052/SEM-011 Triarii gate combination','EXP-066/SEM-012 exact-table identification blocking','EXP-074/SEM-013 actual rating conditional block','All previous pending choices including SEM-001/002/003/009/010','All relation judgments and TP/FP/FN; missing critical pairs remain open','E916 and 64 glyph boundaries','Whole inventory records/fields, metadata/aliases and real graphic ratings','Full scenario/setup/external procedures and dependent full outcomes','20 situations','Full graph/depth/time-budget compliance'],context_acceptance_is_gap_closure=False,owner_opened_report_or_images='unknown',M_POC5A_closed=False,M_POC5A_4_closed=False,new_extractions=0,new_corrections=0)
save(REV/'owner-decision-03.json',decision);dr=ref(REV/'owner-decision-03.json')
runs={}
for run,response in C['responses'].items():
    previous=old['runs'][run]
    merged=previous['scopes']+[dict(s,response=response,decision=dr) for s in scopes if s['id'] in local_ids]
    contexts=previous['context_requirements']+[dict(s,response=response,decision=dr) for s in scopes if s['id'] in context_ids]
    assert len(merged)==63 and len({s['id'] for s in merged})==63 and len(contexts)==3
    runs[run]=dict(response=response,evaluation=C['evaluation'],scopes=merged,context_requirements=contexts,content_group_denominator=66,accepted_scoped_groups=63,pending_content_groups=3,context_group_denominator=8,reviewed_context_groups=3,pending_context_groups=5,context_full_resolution='blocked_source; acceptance of source requirement is not source acquisition or closure',complete_rule_quality='not_assessable',semantic_TP_FP_FN='not_assessable')
new_categories=[dict(id=r['id'],category=r['category'],expectation_id=r['frozen_unit']['expectation_id'],scoped_content=r['frozen_unit']['scoped_content'],status='reviewed',result='correct_in_owner_accepted_scope',reviewer=reviewer,decision=dr,original_unit=r['frozen_unit'],derivation='Only relevant components of accepted EXP-owned scope; not an additional rule point or full-category acceptance.') for r in C['category_units'] if r['frozen_unit']['expectation_id'] in local_ids]
categories=old['category_units']+new_categories
assert len(new_categories)==89 and len(categories)==264 and len({r['id'] for r in categories})==264
accepted_ids={r['id'] for r in runs['first-001']['scopes']}|{r['id'] for r in runs['first-001']['context_requirements']}
pending=[e['id'] for e in C['expectations'] if e['id'] not in accepted_ids]
assert pending==[f'EXP-{n:03}' for n in [10,17,19,40,50,52,66,74]]
overlay=dict(id='M-POC5A-owner-review-overlay-03',decision=dr,prior_overlay=ref(REV/'owner-review-overlay-02.json'),evaluation=C['evaluation'],base_checklist=ref(REV/'checklist.json'),responses=C['responses'],runs=runs,category_units=categories,category_accepted_scope_counts=dict(Counter(r['category'] for r in categories)),category_full_denominators=C['counts']['categories'],pending_expectation_ids=pending,pending_prior_issue_ids=old['pending_prior_issue_ids']+['SEM-011','SEM-012','SEM-013'],inventory_scope_policy='Only accepted EXP-owned source spans within inventory_refs; never whole parents/items/fields inferred through mapping.',illustration_states=dict(expectation_ids=['EXP-054','EXP-057'],status='reviewed_in_exact_scopes',decision=dr,scope='Fire/Move counter sides and Once/Finished marker states only; not tiny ratings or diagram denominator.'),all_output_edges_review='pending',all_locator_review='unchanged',full_semantic_metrics='not_assessable',no_new_gold=True,no_response_changes=True,no_situation_review=True)
save(REV/'owner-review-overlay-03.json',overlay)
save(REV/'current-state-07.json',dict(id='M-POC5A-current-state-07',card='M-POC5A',part='M-POC5A.4a-owner-review',next_part='M-POC5A.4b',status='partial_waiting_review',previous_state=ref(REV/'current-state-06.json'),decision=dr,overlay=ref(REV/'owner-review-overlay-03.json'),evaluation=C['evaluation'],responses=C['responses'],owner_accepted_local_groups_per_answer=63,reviewed_context_requirements_per_answer=3,remaining_pending_expectations=8,pending_expectation_ids=pending,pending_local_ids=['EXP-017','EXP-040','EXP-052'],pending_context_ids=['EXP-010','EXP-019','EXP-050','EXP-066','EXP-074'],remaining_uncompared_expectations=0,context_requirements_still_block_full_results=True,all_relations_and_locators_pending=True,M_POC5A_closed=False,M_POC5A_4_closed=False,resume='Next separate .4b relationships, then .4c locators and .4d residual inventory/pending reconciliation; split before execution as needed. Prior alternatives and EXP-052/066/074 remain open.'))
summary='''# Akceptacja pozytywnego zakresu .4a — 2026-10-11

Właściciel odpowiedział „zatwierdzzm” po objaśnieniu po ludzku i propozycji
przyjęcia 20 zgodnych zakresów oraz wymagania danych scenariusza EXP-064,
z pozostawieniem EXP-052/066/074 otwartych. Literówki nie normalizowano
w dowodzie. Podstawa: nowa owner-decision-03.json i approval-evidence.json
w measurement/M-POC5A-owner-review-003/. Nie poświadczono odczytu obrazów.

Akceptacja obu oryginalnych hashów: EXP-051, EXP-053–063, EXP-065,
EXP-067–073; poprawne wymaganie/blokada źródła EXP-064. Wyłącznie ich
dokładne reviewed_scope. Nie obejmuje całych rekordów/pól, innych klauzul,
grafu, lokatorów, rzeczywistych ratingów, setupu i sytuacji.

Łącznie w każdym wyniku 63/66 lokalnych zakresów przyjętych i 3/8 wymagań
kontekstu przejrzanych. Wymagania nie zamykają pełnych zależnych wyników.
3 lokalne i 5 kontekstu nadal pending, 8 oczekiwań:
EXP-010/017/019/040/050/052/066/074. SEM-001–013 zachowane w ich zakresach;
pozytywna decyzja nie wybiera żadnego wcześniejszego nierozstrzygnięcia.
264 par rubryka/EXP dotyczy tylko przyjętych komponentów i nie daje
dodatkowych punktów reguł ani certyfikatu kategorii.

Nowy stan: current-state-07.json i owner-review-overlay-03.json.
M-POC5A i nadrzędna .4 partial; M-POC5 jedyny next. Następna osobna .4b,
.4c/.4d niewykonane. Cały graf, 64 granice glifów z E916, reszta inwentarza
i pełne metryki/TP/FP/FN niezamknięte. Aktywny budżet unknown.
Nie zmieniono wcześniejszych pakietów, decyzji, źródeł lub odpowiedzi.
'''
path=REV/'owner-review-summary-03.md';assert not path.exists();path.write_text(summary,encoding='utf-8')
save(M/'decision-artifacts.json',dict(artifacts=[ref(REV/f) for f in ['owner-decision-03.json','owner-review-overlay-03.json','current-state-07.json','owner-review-summary-03.md']],semantic_acceptance='actual_owner_exact_scope',owner_reply=reply))
print(json.dumps(dict(local_groups_per_answer=63,reviewed_context_requirements_per_answer=3,pending_expectations=8,category_units=264,protected_files=len(protected),next_part='M-POC5A.4b'),ensure_ascii=False))
