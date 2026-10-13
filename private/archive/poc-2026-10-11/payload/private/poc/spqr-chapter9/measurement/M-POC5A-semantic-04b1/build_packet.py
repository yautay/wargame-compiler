"""Materialize evaluator-authored notes and verified traces; never infer semantics."""
from pathlib import Path
from collections import Counter
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[5]; P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent; REV=P/'reviews/semantic-01'; OUT=REV/'part-04b1'
sys.stdout.reconfigure(encoding='utf-8')
def load(p): return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes(); return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def resolve(o,ptr):
    for k in ptr.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');o=o[int(k)] if isinstance(o,list) else o[k]
    return o
A=load(M/'annotations.json'); C=load(REV/'checklist.json')
PLAN=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json')
ASSIGNED=PLAN['parts'][0]['output_edge_ids']
assert [a[0] for a in A['rows']]==ASSIGNED and len(ASSIGNED)==65
INV=load(P/'evaluation/eval-v1/inventory.json'); IM={i['id']:(n,i) for n,i in enumerate(INV['items'])}
props={r:load(P/f'proposals/{r}/proposal.json') for r in C['responses']}
prov={r:load(P/f'proposals/{r}/provenance.json') for r in C['responses']}
def trace(r,rid):
    t=C['output_records'][r][rid]; obj=t['original_record']; ptr=t['pointer']
    return dict(id=rid,response=C['responses'][r],pointer=ptr,raw_span=t['raw_span'],original_record=obj,
                fields={k:dict(pointer=ptr+'/'+k,raw_span=prov[r]['json_value_spans'][ptr+'/'+k],original_value=v) for k,v in obj.items()})
def invsource(ids):
    out=[]
    for rid in filter(None,ids.split(',')):
        n,i=IM[rid]
        out.append(dict(inventory_id=rid,artifact=ref(P/'evaluation/eval-v1/inventory.json'),pointer=f'/items/{n}',
                        exact_source_span=i.get('source_span',i.get('source_transcription')),
                        source_span_priority='Exact child source_span/source_transcription takes priority over containing evidence transcription; scope narrowed further by manually authored source_scope/target_scope.',
                        evidence=i['evidence']))
    return out
# Independent bounded source blocks from supplied helper regions, not extractor quotes.
regions=load(P/'inputs/v1/helper-regions.json')['regions']
def block(region,start,end=None):
    n=next(n for n,v in enumerate(regions) if v['region_id']==region); v=regions[n]; s=v['text'].index(start); e=v['text'].index(end,s+len(start)) if end else len(v['text'])
    return dict(artifact=ref(P/'inputs/v1/helper-regions.json'),pointer=f'/regions/{n}/text',source=C['source'],pdf_page=v['pdf_page'],region=region,
                character_range=[s,e],literal_helper_text=v['text'][s:e],image=ref(P/v['image']),bbox_pdf_points=v['pdf_bbox'],
                policy='Existing supplied helper transcription checked visually in supplied render; block describes source, not a new locator/glyph certificate.')
boundary={
 'N871':block('pdf-31-context-right-before-9','8.71','8.72'),
 'N872':block('pdf-31-context-right-before-9','8.72','8.73'),
 'N873':block('pdf-31-context-right-before-9','8.73','8.74'),
 'N875':block('pdf-31-context-right-before-9','8.75'),
 'N1011':block('pdf-37-context-left-from-10','10.11','10.12'),
 'N1013':block('pdf-37-context-right','10.13','10.14'),
 'N1014':block('pdf-37-context-right','10.14','10.15'),
 'NCTX846S4':dict(artifact=ref(P/'context/pass-01/evidence/8.46-step-4-helper.txt'),scope=ref(P/'context/pass-01/evidence/8.46-step-4-scope.json'),source=C['source'],pdf_page=27,column='left',bbox_pdf_points=[40,413,300,650],literal_helper_text=(P/'context/pass-01/evidence/8.46-step-4-helper.txt').read_text(encoding='utf-8'),image=ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),policy='Only supplied Step4 crop. Parent heading26, full27, Steps1–3,8.45/CRT not newly acquired or read.')}
OUT.mkdir(exist_ok=True)
rows=[]
for eid,srcids,tgtids,scope,targetscope,necessity,note in A['rows']:
    row=dict(id=eid,source_scope=scope,target_scope=targetscope,source_evidence=invsource(srcids),target_evidence=invsource(tgtids),reviewer=A['reviewer'],
             proposal=note,necessity_and_missing_impact=necessity,authoring=ref(M/'annotations.json'),human_status='waiting_review',human_reviewer=None,runs={})
    for r in C['responses']:
        edge=next((e for e in props[r]['dependencies'] if e['id']==eid),None)
        if edge is None:
            row['runs'][r]=dict(response=C['responses'][r],record_present=False,reviewer=A['reviewer'],status='waiting_review',proposal='Not present in first-001; this edge was added after context. Absence is not a semantic FN without a frozen tuple/owner decision.',not_scored=True,raw_edge_span=None)
            continue
        x=trace(r,eid); endpoints=[v for v in [edge['from'],edge['to']] if v]
        extra_sources=[boundary[v] for v in endpoints if v in boundary]
        if eid=='DCTX846S4-845': extra_sources=[boundary['NCTX846S4']]
        if eid=='D962shock' and r=='first-001': extra_sources=[]
        ids=list(dict.fromkeys([eid]+endpoints+edge['gap_ids']+[q for ep in endpoints for q in C['output_records'][r][ep]['original_record'].get('gap_ids',[])]+edge['evidence_ids']+[q for ep in endpoints for q in C['output_records'][r][ep]['original_record'].get('evidence_ids',[])]))
        row['runs'][r]=dict(response=C['responses'][r],record_present=True,reviewer=A['reviewer'],status='waiting_review',human_reviewer=None,meaning_result='not_assessable',
            evaluator_compared=True,source_scope=scope,target_identity=dict(output_id=edge['to'],candidate=edge['target_candidate'],source_availability='Present only in the bounded source evidence below; unresolved candidates have no target text.'),
            target_scope=targetscope,bounded_independent_source=extra_sources,output_trace={q:trace(r,q) for q in ids},
            direction=dict(observed_from=edge['from'],observed_to=edge['to'] or edge['target_candidate'],assessment='Physical earlier→later for continuation; otherwise referring/using clause→used/qualified target; correct within authored scope.'),
            kind=dict(observed=edge['kind'],assessment='owner_kind_decision_required' if eid in ['D9161011','D968column','DCTX923-S4'] else 'supported_in_bounded_scope'),
            explicitness=dict(observed=edge['explicitness'],assessment='owner_label_decision_required' if eid=='D967966' else 'supported_in_bounded_scope',interpretation='Explicit source reference/name for mention/continuation; implicit linkage when no numbered target is stated or relation is inferred from applicable constraints. D967966 named operation is separately disputed.'),
            necessity=necessity,missing_target_impact=dict(observed=edge['impact_if_missing'],evaluator_assessment=necessity,scope_warning='Generic target supplied/false is availability, not proof that a hypothetically missing necessary target would be nonblocking. Accept only scoped tuple/role; blanket impact false excluded for operative source-present edges.'),
            proposed_assessment='separate_issue_decision' if eid in A['separate_issue_edge_ids'] else 'supported_bounded_tuple_or_occurrence',comparison=note,
            exclusions=['Whole rule/node/field acceptance','Unreviewed aliases, external target source identity, real ratings/setup/20 situations','All earlier SEM-001–013 and pending EXP scopes retained','Full target execution/graph certificate','E916 and64glyph-boundary review','Blanket impact false for necessary source-present targets'],uncertainties=[necessity,'No new human decision; pending is neither TP nor certain FP.'])
    row['output_values_identical_between_runs']=next((e for e in props['first-001']['dependencies'] if e['id']==eid),None)==next((e for e in props['context-01']['dependencies'] if e['id']==eid),None)
    rows.append(row)
frozen=[]
for f in C['frozen_relations']:
    if f['category'] not in ['confirmed_execution_relations','mentions','continuations']: continue
    obj=f['frozen_record']; fid=f['id']; runs={}
    for r in C['responses']:
        prev=f['run_comparison'][r]; candidates=prev.get('candidate_output_ids',prev.get('output_ids',[]))
        ends=prev.get('mapped_output_endpoints',[])
        if f['category']=='mentions':
            ends={'DEP-034':['N923ex'],'DEP-035':['N932ex'],'DEP-037':['R961'],'DEP-043':['N914diagram','R914'],'DEP-044':['R966','N966diagram'],'DEP-063':['N953ex'],'DEP-067-1':['R966']}[fid]
        if f['category']=='continuations':
            candidates=[{'DEP-090':'Dcont-R911','DEP-091':'Dcont-table914','DEP-092':'Dcont-R914','DEP-093':'Dcont-R924','DEP-094':'Dcont-R966','DEP-095':'Dcont-R991','DEP-096':'Dcont-R996b'}[fid]]
            # Original two locator nodes and owner content are traced explicitly.
            ce=next(e for e in props[r]['dependencies'] if e['id'] in candidates)
            ends=[ce['from'],ce['to']]
            for ep in ends[:]:
                content=C['output_records'][r][ep]['original_record']['content']['value']
                ends += [v for k,v in content.items() if k in ['owner_rule_id','owner_node_id']]
        scope_note=A['frozen_extra_notes'].get(fid)
        if scope_note is None:
            mapped=next(row for row in rows if row['id'] in candidates)
            scope_note=mapped['proposal']+' '+mapped['necessity_and_missing_impact']
        ids=list(dict.fromkeys(candidates+ends))
        runs[r]=dict(response=C['responses'][r],reviewer=A['reviewer'],status='waiting_review',evaluator_compared=True,human_reviewer=None,meaning_result='not_assessable',
                     original_closed_structural_observation=prev,output_trace={q:trace(r,q) for q in ids},proposal=scope_note,
                     proposed_assessment='missing_record_retained_prose_or_combination_pending' if prev['tuple_status']=='missing_tuple' else ('kind_difference_candidate' if prev['tuple_status']=='different_kind_candidate' else 'supported_exact_frozen_scope'),
                     scopes_excluded=['No automatic semanticFN/TP','External aliases/identity not inferred','Physical continuation/mention not executiongold','All prior decisions/pending unchanged'])
    frozen.append(dict(id=fid,category=f['category'],evaluation=ref(P/'evaluation/eval-v1/dependencies.json'),evaluation_pointer=f['evaluation_pointer'],frozen_record=obj,reviewer=A['reviewer'],human_status='waiting_review',runs=runs))
assert len(frozen)==22
summary=dict(assigned_distinct_ids=65,assigned_occurrences=125,assigned_occurrences_per_answer={'first-001':60,'context-01':65},evaluator_compared_occurrences=125,evaluator_compared_distinct_ids=65,
             positive_bounded_ids=[r['id'] for r in rows if r['id'] not in A['separate_issue_edge_ids']],separate_issue_ids=A['separate_issue_edge_ids'],
             positive_bounded_occurrences=116,separate_issue_occurrences=9,extra_frozen_tuples=22,extra_frozen_per_answer=22,
             frozen_explicit_proposed_bounded_support=5,frozen_implicit_missing_records=3,frozen_mention_proposed_occurrence=2,frozen_mentions_kind_difference=1,frozen_mentions_missing_records=4,frozen_physical_continuations_proposed_support=7,
             packet_available_assigned_occurrences=125,owner_actual_open_or_read='unknown',new_human_reviewed_occurrences=0,owner_pending_occurrences=125,
             all_4b_occurrences=257,remaining_uncompared_4b_occurrences=132,remaining_parts_4b2_4b3={'M-POC5A.4b2':60,'M-POC5A.4b3':72},
             TP_gold='not_assessable',TP_output='not_assessable',FP='not_assessable',FN='not_assessable',precision='not_assessable',recall='not_assessable',unconfirmed_candidates_not_gold=105,
             owner_accepted_local_groups_per_answer=63,reviewed_context_requirements_per_answer=3,pending_expectation_ids=load(REV/'current-state-08.json')['pending_expectation_ids'])
payload=dict(id='M-POC5A.4b1-comparisons-01',card='M-POC5A.4b1',status='partial_waiting_review',evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
             scope_plan=ref(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json'),estimate=ref(M/'start.json'),method=A['method'],
             source_span_policy='Manual exact scope precedes source_span/source_transcription and then containing transcription/envelope. Parent crosswalk only locates candidates, never proves child meaning.',
             source_images_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in range(31,38)]+[ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png')],
             summary=summary,relationships=rows,frozen_tuple_comparisons=frozen,previous_state=ref(REV/'current-state-08.json'),owner_decisions=[ref(REV/f'owner-decision-{n:02}.json') for n in [1,2,3]],owner_overlay=ref(REV/'owner-review-overlay-03.json'),new_owner_decisions=[],
             inherited_issues=[f'SEM-{n:03}' for n in range(1,14)],limits=C['limits'],limitations=C['limitations'],other_parts_executed=False)
save(OUT/'comparisons.json',payload)
issues=[
 dict(id='SEM-014',classes=['błędna interpretacja','brak kontekstu'],scope=['D9621013','DCTX846S4-1013','D962shock'],proposal='D9621013 ma poprawne jawne użycie10.13, lecz false/emptygap nie wyraża zagnieżdżonej blokady within-stack6.68#6. NodeN1013 i G-D1013stack zachowują blokadę osobno; nowa Step4→10.13 ma true. Proponuję rozdzielić poprawny endpoint od oceny wystarczalności impact. Ogólne false bo cel dostępny nie ocenia kontrfaktycznego braku koniecznego celu.',impact='Full Roman stack allocation cannot be certified from target_status. R962→Step4→10.13→missing6.68#6 is3edges, third source not acquired; expansion stopped at2.',uncertainty='Owner must decide adequacy of distributed block declarations; no actual wrong allocation asserted.'),
 dict(id='SEM-015',classes=['błędna interpretacja'],scope=['DEP-037','D961stack'],proposal=A['frozen_extra_notes']['DEP-037'],impact='Table_use is not full tuple match for the frozen mention; no final precision/recall award.',uncertainty='Actual chart source and broader execution remain unknown; limited extra frozenmention comparison only.'),
 dict(id='SEM-016',classes=['błędna interpretacja','niejednoznaczność'],scope=['D9161011','D967966','D968column'],proposal='Tożsamości i kierunki poparte. Właściciel rozstrzyga definition/procedure_use dla TQcheck, implicit/explicit dla nazwanego MLE-use oraz mention/condition dla inColumn exclusion. Format nie precyzuje granicy tych facetów; nie uznać etykiet przez same target_status lub nazwy.',impact='Kind/explicitness affects tuple scoring; source-local operations may remain supported independently.',uncertainty='Bounded classification candidates, not confirmed wrong reads or certainFP.'),
]
for i in issues:
    i.update(status='waiting_review',reviewer=A['reviewer'],human_reviewer=None,evaluation=C['evaluation'],responses=C['responses'],source=C['source'],comparison_packet=ref(OUT/'comparisons.json'),new_owner_decision=None)
save(OUT/'issues.json',dict(issues=issues,inherited_pending=[f'SEM-{n:03}' for n in range(1,14)],SEM_004_additional_evidence='DCTX923-S4 comparison in packet; remains pending with bounded side/factor/cap support.',structural_missing_pairs=['DEP-NEW-001','DEP-NEW-002','DEP-NEW-003','DEP-034','DEP-035','DEP-043','DEP-067-1'],confirmed_semantic_error_counts='not_assessable',wrong_read='not_assessable',policy='No automatic conversion structural missing→semanticFN; retained prose assessed separately. No previous issue closed.'))
head=['# M-POC5A.4b1 — rzeczywiste porównania relacji','','Recenzent propozycji: Codex. Znaczenie akceptuje właściciel; wszystkie nowe decyzje waiting_review.','',f"65 ID /125 wystąpień: first60, context65. Dodatkowo22 zamrożone pary osobno dla obu odpowiedzi. 60 ID/116 wystąpień ma pozytywną propozycję w dokładnym ograniczonym zakresie;5 ID/9 wystąpień wydzielono do decyzji. To nie liczby poprawnych całych rekordów/TP.",'',*[f"{r}: SHA-256 `{v['sha256']}`, {v['bytes']} bajtów." for r,v in C['responses'].items()],'',f"eval-v1 `{C['evaluation']['sha256']}`; źródło PDF `{C['source']['sha256']}`.",'','[Pełne porównania JSON](comparisons.json): osobne oba hashe, source/targetscope, dosłowne źródła i zapisy modelu, pointers, bajty [start,end), SHA-256 rekordów/pól, gapy, dowody i wyłączenia.','']
lines=head+['## Każde przypisane ID','']
for row in rows:
    lines += [f"### {row['id']}",'','Źródło: '+row['source_scope'],'','Cel: '+row['target_scope'],'','Potrzeba/konsekwencja braku: '+row['necessity_and_missing_impact'],'','Porównanie/propozycja: '+row['proposal'],'']
    for r,x in row['runs'].items():
        if not x['record_present']: lines += [f'**{r}:** brak nowej relacji przed context; nie automatyczneFN.',''];continue
        t=x['output_trace'][row['id']];s=t['raw_span'];e=t['original_record']
        lines += [f"**{r}:** `{t['pointer']}`, bajty [{s['start_byte']},{s['end_byte_exclusive']}), fragment SHA-256 `{s['sha256']}`.",'',f"Zapis modelu: `{e['from']}→{e['to'] or 'candidate'}`, `{e['kind']}/{e['explicitness']}`, `{e['target_status']}`, blocks_full_result=`{e['impact_if_missing']['blocks_full_result']}`.",'', 'Uzasadnienie modelu (osobno od oceny): '+e['rationale'],'']
    for which in ['source_evidence','target_evidence']:
        for v in row[which]:
            span=v['exact_source_span']
            quotes=[span] if span else [e.get('source_span',e.get('transcription')) for e in v['evidence']]
            lines += [f"{which}: `{v['inventory_id']}` / `{v['pointer']}`; dokładny oceniany zakres podano wyżej. Koperta nie poszerza childscope.",'']
            for quote in filter(None,quotes): lines += ['> '+quote.replace('\n','\n> '),'']
    # Boundary/context source is printed separately from extractor claims.
    seen=set()
    for x in row['runs'].values():
        for v in x.get('bounded_independent_source',[]):
            key=(v['artifact']['path'],v.get('pointer',''))
            if key in seen: continue
            seen.add(key); lines += [f"Dostarczone źródło: `{v['artifact']['path']}`, pointer `{v.get('pointer','whole bounded helper')}`, hash `{v['artifact']['sha256']}`.",'','> '+v['literal_helper_text'].replace('\n','\n> '),'']
    lines += ['Wyłączenia: całe rekordy i nieprzejrzane pola, aliases/sourceidentity, realne setup/ratingi,20sytuacji, wcześniejsze pending, lokatory/glyphy i pełny graf. Dla koniecznych dostępnych celów nie przyjmujemy blankietowego impact=false.','']
lines += ['##22 zamrożone pary — oddzielne porównania obu hashów','']
for f in frozen:
    lines += [f"### {f['id']} — {f['category']}",'',f"eval-v1 pointer `{f['evaluation_pointer']}`. Dokładne źródła/authorizing scope w comparisons.json; nie szersze mapowanie parent.",'']
    for r,x in f['runs'].items(): lines += [f"**{r}**: {x['original_closed_structural_observation']['tuple_status']}. "+x['proposal'],'']
tail=['##Granice wyniku','','105 candidates nie staje się gold. Nowe edges osobno, bez punktów za nowość. PełneTP_gold/TP_output/FP/FN/precision/recall not_assessable. 132 wystąpienia .4b2/.4b3 czekają na osobne sesje.','', 'Właścicielowi udostępniono pakiet125 wystąpień; faktyczny odczyt/otwarcie unknown, nowe humanreview0, pending125. Dodatkowe22pary/hash także waiting_review. Dawne63lokalne/3wymagania source na hash bez zmiany; EXP-010/017/019/040/050/052/066/074 i SEM-001–013 pozostają otwarte.','', '1 dodatkowa strona/1reguła/0tabel,1runda context/0korekt;0pełnych domknięć,4częściowe uzupełnienia i4nowe deklaracje. Trzeciego źródła nie pozyskano, stop rozszerzania na2. Czysty kontekst/ekspozycja unknown, listing/path discovery poza allowlistą potwierdzony, treści oceny nie zaobserwowano. Nie dowodzi skażenia ani izolacji. Aktywny czas/budżet/config/tokeny/cena unknown.','', 'Następny krok: decyzje dla owner-focus i wcześniejszych pending; potem osobna .4b2, oszacowana przed wykonaniem; .4b3/.4c/.4d później. M-POC5A/.4/.4b partial; M-POC5 jedyny next.','']
(OUT/'comparisons.md').write_text('\n'.join(lines+tail),encoding='utf-8')
(OUT/'review.md').write_text('\n'.join(head+['Wykonano ręczne porównanie wszystkich65przypisanychID i22zamrożonychpar w obu hashach, z dostarczonym tekstem/rendrami; skrypty wiążą ślady.','', '[Czytelne porównania](comparisons.md), [pakiet decyzji właściciela](owner-focus.md), [kwestie](issues.json).','', 'Nie wykonywano .4b2/.4b3 jako partii. D961stack występuje wyłącznie jako wymagany dodatkowy frozenmention comparison; pozostały zakres .4b3 pozostaje przypisany.','']+tail),encoding='utf-8')
save(M/'packet-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False))
