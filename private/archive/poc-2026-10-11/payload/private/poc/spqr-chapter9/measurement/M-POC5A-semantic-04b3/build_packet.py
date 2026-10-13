"""Attach manually reviewed clauses to original records without altering inputs."""
from pathlib import Path
import json,hashlib,copy
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
R=P/'reviews/semantic-01';OUT=R/'part-04b3'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
A=load(M/'annotations.json');C=load(R/'checklist.json');old=load(R/'current-state-13.json')
assigned=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json')['parts'][2]['output_edge_ids']
assert [x[0] for x in A['rows']]==assigned and len(assigned)==36
props={r:load(P/f'proposals/{r}/proposal.json') for r in C['responses']}
prov={r:load(P/f'proposals/{r}/provenance.json') for r in C['responses']}
im={x['id']:(i,x) for i,x in enumerate(load(P/'evaluation/eval-v1/inventory.json')['items'])}
regions=load(P/'inputs/v1/helper-regions.json')['regions']
def block(region,start,end=None):
    idx,x=next((i,x) for i,x in enumerate(regions) if x['region_id']==region)
    a=x['text'].index(start);b=x['text'].index(end,a+len(start)) if end else len(x['text']);t=x['text'][a:b]
    return dict(artifact=ref(P/'inputs/v1/helper-regions.json'),pointer=f'/regions/{idx}/text',region=region,pdf_page=x['pdf_page'],character_range=[a,b],
        literal_helper_text=t,utf8_excerpt_sha256=hashlib.sha256(t.encode()).hexdigest(),image=ref(P/x['image']),bbox_pdf_points=x['pdf_bbox'],source=C['source'],
        locator_policy='Supplied helper visually checked against existing supplied image; authored exact source_scope leads before broader block/crosswalk. No glyph/bbox certification.')
blocks={
 'R95note':block('pdf-34-core-right','DESIGN NOTE:','9.51'),
 'R951':block('pdf-34-core-right','9.51','9.52'),
 'R952':block('pdf-34-core-right','9.52','9.53'),
 'R953':block('pdf-34-core-right','9.53','EXAMPLE:'),
 'R961':block('pdf-35-core-left','9.61','9.62'),
 'R962':block('pdf-35-core-left','9.62','9.63'),
 'R963':block('pdf-35-core-left','9.63','9.64'),
 'R964':block('pdf-35-core-left','9.64','9.65'),
 'R966a':block('pdf-35-core-left','9.66'),
 'R966b':block('pdf-35-core-right','may move sideways','9.67'),
 'R967':block('pdf-35-core-right','9.67','9.68'),
 'R968':block('pdf-35-core-right','9.68','9.7 ROMAN'),
 'R971':block('pdf-35-core-right','9.71','9.72'),
 'R972':block('pdf-35-core-right','9.72'),
 'R983':block('pdf-36-core-left','9.83','9.84'),
 'R987':block('pdf-36-core-left','9.87','9.9 THE'),
 'R993':block('pdf-36-core-right','9.93','9.94'),
 'R994':block('pdf-36-core-right','All BI units start','9.95'),
 'R995':block('pdf-36-core-right','9.95','9.96'),
 'R996note':block('pdf-36-core-right','DESIGN NOTE: The chariots','Gallic Chariot'),
 'R996a':block('pdf-36-core-right','Gallic Chariot','Each CH unit'),
 'R996b1':block('pdf-36-core-right','Each CH unit'),
 'R996b2':block('pdf-37-core-left','unit for stacking','LI mounted on CH'),
 'R996d':block('pdf-37-core-left','LI mounted on CH'),
 'N1011':block('pdf-37-context-left-from-10','10.11','10.12'),
 'N875':block('pdf-31-context-right-before-9','8.75'),
 'N871':block('pdf-31-context-right-before-9','8.71','8.72')}
def trace(run,rid):
    x=C['output_records'][run][rid];ptr=x['pointer'];obj=x['original_record']
    return dict(id=rid,response=C['responses'][run],pointer=ptr,raw_span=x['raw_span'],original_record=obj,
        fields={k:dict(pointer=ptr+'/'+k,raw_span=prov[run]['json_value_spans'][ptr+'/'+k],original_value=v) for k,v in obj.items()})
OUT.mkdir(exist_ok=False);rows=[]
for eid,inv_ids,bids,source_scope,target_scope,need,note,issue in A['rows']:
    row=dict(id=eid,source_scope=source_scope,target_scope=target_scope,necessity_and_missing_impact=need,proposal=note,
        source_evidence=[dict(inventory_id=i,artifact=ref(P/'evaluation/eval-v1/inventory.json'),pointer=f'/items/{im[i][0]}',exact_child_evidence=im[i][1]['evidence'],gold_status='Crosswalk is not new gold/acceptance.') for i in inv_ids.split(',') if i],
        bounded_independent_source=[blocks[k] for k in bids],target_source_actual=None,
        target_source_policy='Actual requested target content absent or partial framework only. Named requirement is not target contents/alias identity. See individually authored target_scope.',
        reviewer=A['reviewer'],authoring=ref(M/'annotations.json'),human_status='waiting_review',human_reviewer=None,separate_issue=issue,
        historical_component_decision=ref(R/'owner-decision-05.json') if eid=='D961stack' else None,runs={})
    vals=[]
    for run,prop in props.items():
        edge=next(x for x in prop['dependencies'] if x['id']==eid);assert edge['to'] is None;vals.append(edge)
        src=C['output_records'][run][edge['from']]['original_record']
        ids=list(dict.fromkeys([eid,edge['from'],*edge['gap_ids'],*edge['evidence_ids'],*src.get('gap_ids',[]),*src.get('evidence_ids',[])]))
        kind_assessment='supported_as_bounded_required_role_not_actual_target_content'
        explicit_assessment='supported_explicit_named_requirement_or_implicit_definition_dependency'
        if eid=='D951terrain':
            kind_assessment='explicit cost requirement supported; specific table-use target inferred, separate owner decision'
            explicit_assessment='normal cost explicit; specific chart reference not explicit in9.51; SEM-018'
        if eid=='D961stack':
            kind_assessment='mention already owner-decided inSEM-015, rawtable_use retained as immutable observation; no repeated kind decision'
        partial=[blocks[k] for k in bids if k.startswith('N')]
        if eid=='D961stack':full='Actual stack legality with unsupplied exceptions remains blocked; summary lookup itself is not an execution prerequisite.'
        elif eid in ['D996supply','D996tables']:full='Local exclusion/ignore nonblocking; ordinary supply/table identification and complete fire/combat execution not certified.'
        else:full='Dependent full execution/real qualification needs missing applicable target data; does not blanket-block all source-local operations.'
        row['runs'][run]=dict(response=C['responses'][run],record_present=True,reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',evaluator_compared=True,meaning_result='not_assessable',
            source_scope=source_scope,target_scope=target_scope,target_identity=dict(output_id=None,candidate=edge['target_candidate'],actual_target_content='not_supplied_in_full',alias_identity='not_assessable'),
            direction=dict(observed_from=edge['from'],observed_to=edge['target_candidate'],assessment='Source clause -> required/modified/excepted named concept; D961stack summary mention and D951terrain inferred table distinguished in authored notes.'),
            kind=dict(observed=edge['kind'],assessment=kind_assessment),explicitness=dict(observed=edge['explicitness'],assessment=explicit_assessment,basis=note),
            necessity=need,missing_target_impact=dict(observed=edge['impact_if_missing'],evaluator_scope=need,full_dependent_result=full,
                local_source_operator='Judge local operator using given relevant facts; do not invent missing eligibility or actual tables/setup.',classification='owner_scope_decision_required' if issue else 'supported_only_in_authored_bounded_scope'),
            output_trace={i:trace(run,i) for i in ids},supplemental_supplied_context=partial,comparison=note,
            proposed_assessment='separate_scoped_decision' if issue else 'supported_bounded_requirement_and_relation_role',
            historical_kind_decision_unchanged=(eid=='D961stack'),
            exclusions=['Whole source/target records and unreviewed fields','Absent target content, numeric values, actual chart/setup and alias identities',
                'Blanket blocking of known local operators/exceptions when relevant facts given','Earlier pending issues/expectations and excluded fields of prior decisions',
                'Full movement/fire/combat outcomes, glyph/locator/rating checks,20situations, newgold and final TP/FP/FN/precision/recall'],
            uncertainties=['Target content missing or only partial supplied framework','New decisions await owner; no automatic TP/FP','No demonstrated wrong played result from missing context alone'])
    row['output_values_identical_between_runs']=vals[0]==vals[1]
    ga={run:[row['runs'][run]['output_trace'][g]['original_record'] for g in vals[i]['gap_ids']] for i,run in enumerate(props)}
    row['assigned_gap_values_identical_between_runs']=ga['first-001']==ga['context-01']
    row['run_difference_assessment']='Assigned edge and its gaps unchanged in both original results; separately traced source records can contain prior context links. No new context in this review.'
    rows.append(row)
assert all(x['output_values_identical_between_runs'] and x['assigned_gap_values_identical_between_runs'] for x in rows)
positive=[x['id'] for x in rows if not x['separate_issue']]
summary=dict(assigned_distinct_ids=36,assigned_occurrences=72,per_answer={'first-001':36,'context-01':36},evaluator_compared_occurrences=72,
    positive_bounded_ids=positive,positive_bounded_occurrences=68,separate_issue_ids=A['separate_issue_edge_ids'],separate_issue_occurrences=4,
    owner_available_occurrences=72,new_owner_reviewed_occurrences=0,owner_pending_occurrences=72,owner_actual_open_or_read='unknown',
    previously_decided_kind_components_in_this_part=2,previous_owner_decided_assigned_scopes=185,total_evaluator_compared_assigned_occurrences=257,remaining_uncompared_occurrences=0,
    pending_expectation_ids=old['pending_expectation_ids'],unconfirmed_candidates_not_gold=105,
    TP_gold='not_assessable',TP_output='not_assessable',FP='not_assessable',FN='not_assessable',precision='not_assessable',recall='not_assessable')
packet=dict(id='M-POC5A.4b3-comparisons-01',card='M-POC5A.4b3',status='partial_waiting_review',evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
    scope_plan=ref(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json'),estimate=ref(M/'start.json'),method=A['method'],
    source_span_policy='Exact authored source_scope leads before containing source blocks and inventory crosswalk; mapping does not confer acceptance.',
    source_images_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in [31,34,35,36,37]],summary=summary,relationships=rows,
    previous_state=ref(R/'current-state-13.json'),owner_decision=ref(R/'owner-decision-06.json'),owner_overlay=ref(R/'owner-review-overlay-06.json'),
    new_owner_decisions=[],inherited_issues=old['unresolved_issue_ids'],prior_dispositions=old['issue_dispositions'],limits=C['limits'],limitations=C['limitations'],other_parts_executed=False)
save(OUT/'comparisons.json',packet)
issues=copy.deepcopy(A['new_issues'])
for issue in issues:issue.update(status='waiting_review',reviewer=A['reviewer'],human_reviewer=None,evaluation=C['evaluation'],responses=C['responses'],source=C['source'],comparison_packet=ref(OUT/'comparisons.json'),actual_wrong_played_outcome='not_demonstrated')
save(OUT/'issues.json',dict(issues=issues,inherited_pending=old['unresolved_issue_ids'],previous_dispositions_preserved=old['issue_dispositions'],
    wrong_read='not_assessable',confirmed_semantic_error_counts='not_assessable',policy='Two narrowly scoped proposals. No old pending or full dependent outcome closed; D961stack kind is already decided and not reasked.'))
save(OUT/'presentation.json',dict(card='M-POC5A.4b3',positive_scope=dict(ids=positive,occurrences=68,per_answer={'first-001':34,'context-01':34},
    includes=['Exact authored clause and source→target requirement','Bounded kind/explicitness in individual notes, absent target not certified','Missing impact only for full dependent execution or exact local nonblocking exclusion'],excludes=rows[0]['runs']['first-001']['exclusions']),
    separate_issues=[dict(id=x['id'],ids=x['scope'],occurrences=x['occurrences']) for x in issues],owner_available_occurrences=72,evaluator_compared_occurrences=72,new_owner_reviewed_occurrences=0,owner_pending_occurrences=72,
    previously_decided_kind_components=2,actual_owner_file_open_or_read='unknown',proposal_only=True,next_after_owner_decision='Separate M-POC5A.4c after its own estimate/split; remaining old pending/excluded fields stay open.'))
lines=['# M-POC5A.4b3 — wszystkie36ID porównane w obu wynikach','',A['method'],'',
    '72 wystąpienia:36/36;68 pozytywnych ograniczonych propozycji i4 wystąpienia z dwiema osobnymi kwestiami. Wszystkie nowe oceny waiting_review. Rodzaj D961stack pozostaje już rozstrzygnięty jako mention.',
    '',*[f"{run}: SHA-256 `{a['sha256']}`, {a['bytes']} bajtów." for run,a in C['responses'].items()],
    '',f"eval-v1 `{C['evaluation']['sha256']}`; PDF `{C['source']['sha256']}`.",
    '', '[Pełny ślad pól, źródeł i bajtów](comparisons.json). Kandydat modelu nie jest treścią źródła celu.','']
for row in rows:
    lines += [f"## {row['id']}",'','Źródło / dokładny zakres: '+row['source_scope'],'','Cel / dostępność: '+row['target_scope'],'','Konieczność / wpływ: '+row['necessity_and_missing_impact'],'','Porównanie / propozycja: '+row['proposal'],'']
    for run,x in row['runs'].items():
        t=x['output_trace'][row['id']];e=t['original_record'];sp=t['raw_span']
        lines += [f"**{run}:** `{t['pointer']}`; bajty [{sp['start_byte']},{sp['end_byte_exclusive']}), SHA-256 `{sp['sha256']}`.",'',
            f"Zapis modelu: `{e['from']}→candidate`, `{e['kind']}/{e['explicitness']}`, unresolved, blocks_full_result=`{e['impact_if_missing']['blocks_full_result']}`.",'',
            'Dosłowny kandydat modelu: '+json.dumps(e['target_candidate'],ensure_ascii=False),'','Uzasadnienie modelu: '+e['rationale'],'',
            'Wpływ zapisany przez model: '+json.dumps(e['impact_if_missing'],ensure_ascii=False),'','Ocena rodzaju: '+x['kind']['assessment'],'','Ocena jawności: '+x['explicitness']['assessment'],'',
            'Ocena brakującego celu: '+x['missing_target_impact']['full_dependent_result'],'']
        for gid in e['gap_ids']:
            g=x['output_trace'][gid]['original_record'];lines += ['Dosłowny gap: '+json.dumps(g,ensure_ascii=False),'']
    for b in row['bounded_independent_source']:
        lines += [f"Niezależny dostarczony helper `{b['artifact']['path']}`, `{b['pointer']}`, znaki [{b['character_range'][0]},{b['character_range'][1]}), hash wycinka `{b['utf8_excerpt_sha256']}`. Oceniana klauzula to source_scope, nie cała koperta.",'',
            '> '+b['literal_helper_text'].replace('\n','\n> '),'']
    lines += ['Wyłączenia: całe rekordy/pola, rzeczywista treść brakujących celów i aliasy, wcześniejsze pending, pełne wyniki, setup/ratingi/glify,20sytuacji i metryki.','']
lines += ['## Granice wyniku','',
    '36 przypisanych krawędzi i ich gapy identyczne między odpowiedziami; oba wyniki mają osobne pełne ślady. Wcześniej dostarczone10.11/8.75 opisują fragment framework TQ, nie actual chart; uwzględniono częściową dostępność.',
    'Udostępniono72, porównano72, nowych decyzji właściciela0, pending72. Faktyczny odczyt/otwarcieunknown. Poprzednie185 dokładnych zakresów mają decyzje; dodatkowa wcześniejsza decyzja kindD961stack nie jest ponownie pytana ani liczonajako nowe rozstrzygnięcie.',
    'Łącznie w przydziale .4b porównano257 wystąpień (126/131). To nie certyfikat wszystkich pól, całego grafu, brakujących frozen pairs lub gold. Osiem starych oczekiwań iSEM-001–013 w pozostałych zakresach otwarte; scopedSEM-014–017 zachowane. NoweSEM-018/019waiting_review.',
    '105 candidates nie staje sięgold; TP/FP/FN/precision/recall not_assessable. Nie zmieniono źródeł, odpowiedzi, eval-v1, dawnych artefaktów ani limitów. Brak nowych ekstrakcji/korekt i sytuacji.',
    'Kontekst1strona/1reguła/0tabel,1runda/0korekt;0pełnych domknięć,4częściowe aktualizacje/4nowe deklaracje, stop ekspansji na2. Izolacja dawnego context-01: listing/path pozaallowlistą potwierdzony, odczyt treści oceny niezaobserwowany, exposure/cleancontextunknown. Aktywne czasy/selektory/tokens/cena/budżetunknown.',
    'Po decyzjach .4b3 kolejna osobna .4c z własnym oszacowaniem i ewentualnym podziałem przed pracą. .4c/.4d nie wykonano; M-POC5A/.4/.4b partial, M-POC5 jedyny next.','']
(OUT/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'review.md').write_text('# M-POC5A.4b3 — rzeczywisty przegląd wykonany\n\n'+A['method']+'\n\n'+
    'Rozliczono36ID/72wystąpienia:68 ograniczonych pozytywnych propozycji,4 w osobnych kwestiachSEM-018/019. Żadna nowa propozycja nie jest automatycznie accepted.\n\n'+
    '[Każde porównanie](comparisons.md), [surowe ślady obu odpowiedzi](comparisons.json), [decyzje po ludzku](owner-focus.md), [kwestie](issues.json).\n\n'+'\n\n'.join(lines[-8:]),encoding='utf-8')
save(M/'packet-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False))
