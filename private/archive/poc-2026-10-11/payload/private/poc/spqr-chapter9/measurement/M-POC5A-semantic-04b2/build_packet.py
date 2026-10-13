"""Materialize manually authored comparisons with independently bounded source."""
from pathlib import Path
import copy,json,hashlib
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
R=P/'reviews/semantic-01';OUT=R/'part-04b2'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
A=load(M/'annotations.json');C=load(R/'checklist.json');prior=load(R/'current-state-11.json')
plan=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json')
assigned=plan['parts'][1]['output_edge_ids'];assert [x[0] for x in A['rows']]==assigned and len(assigned)==30
props={run:load(P/f'proposals/{run}/proposal.json') for run in C['responses']}
prov={run:load(P/f'proposals/{run}/provenance.json') for run in C['responses']}
inv=load(P/'evaluation/eval-v1/inventory.json');im={x['id']:(i,x) for i,x in enumerate(inv['items'])}
regions=load(P/'inputs/v1/helper-regions.json')['regions']
def block(region,start,end=None):
    idx,x=next((i,x) for i,x in enumerate(regions) if x['region_id']==region)
    a=x['text'].index(start);b=x['text'].index(end,a+len(start)) if end else len(x['text'])
    text=x['text'][a:b]
    return dict(artifact=ref(P/'inputs/v1/helper-regions.json'),pointer=f'/regions/{idx}/text',region=region,pdf_page=x['pdf_page'],
        character_range=[a,b],literal_helper_text=text,utf8_excerpt_sha256=hashlib.sha256(text.encode('utf-8')).hexdigest(),
        image=ref(P/x['image']),bbox_pdf_points=x['pdf_bbox'],source=C['source'],
        locator_policy='Supplied transcription checked in existing supplied image. Manual source_scope is narrower than the containing block; no glyph-level locator certificate.')
blocks={
 'R911a':block('pdf-31-core-right','9.11'),
 'R911b':block('pdf-32-core-left','3. After','DESIGN NOTE:'),
 'R912':block('pdf-32-core-left','9.12','9.13'),
 'R913':block('pdf-32-core-left','9.13','DESIGN NOTE: Several'),
 'R914priority':block('pdf-32-core-right','Each Elephant Rampage','EXAMPLE:'),
 'R914table':block('pdf-32-core-left','1–6'),
 'R914caption':block('pdf-32-core-right','EXAMPLE:','A rampaging Elephant'),
 'R914move':block('pdf-32-core-right','A rampaging Elephant','The player now rolls'),
 'R914end':block('pdf-32-core-right','A leader stacked','Rampaging elephants'),
 'R915':block('pdf-33-core-left','9.15','9.16'),
 'R916':block('pdf-33-core-left','9.16','9.17'),
 'R917':block('pdf-33-core-left','9.17','HISTORICAL NOTE:'),
 'R919':block('pdf-33-core-left','9.19','HISTORICAL NOTE:'),
 'R921':block('pdf-33-core-right','9.21','9.22'),
 'R922':block('pdf-33-core-right','9.22','9.23'),
 'R923':block('pdf-33-core-right','9.23','9.24'),
 'R924lineA':block('pdf-33-core-right','• When determining lines'),
 'R924lineB':block('pdf-34-core-left','the interruption','9.3 LIGHT'),
 'R924stack':block('pdf-33-core-right','• See 6.69','• When determining lines'),
 'R931':block('pdf-34-core-left','9.31','9.32'),
 'R932':block('pdf-34-core-left','9.32','9.4 PHALANX'),
 'R941':block('pdf-34-core-left','9.41','DESIGN NOTE:'),
 'N1011':block('pdf-37-context-left-from-10','10.11','10.12'),
 'N1013':block('pdf-37-context-right','10.13','10.14'),
 'N871':block('pdf-31-context-right-before-9','8.71','8.72'),
 'N872':block('pdf-31-context-right-before-9','8.72','8.73'),
 'N873':block('pdf-31-context-right-before-9','8.73','8.74'),
 'N875':block('pdf-31-context-right-before-9','8.75')}
step=dict(artifact=ref(P/'context/pass-01/evidence/8.46-step-4-helper.txt'),scope=ref(P/'context/pass-01/evidence/8.46-step-4-scope.json'),
    literal_helper_text=(P/'context/pass-01/evidence/8.46-step-4-helper.txt').read_text(encoding='utf-8'),
    image=ref(P/'context/pass-01/evidence/8.46-step-4-pdf-27.png'),source=C['source'],pdf_page=27,
    policy='Only previously supplied Step4 crop; no new page/source, no earlier steps or actual CRT.')
def trace(run,rid):
    x=C['output_records'][run][rid];ptr=x['pointer'];obj=x['original_record']
    return dict(id=rid,response=C['responses'][run],pointer=ptr,raw_span=x['raw_span'],original_record=obj,
        fields={k:dict(pointer=ptr+'/'+k,raw_span=prov[run]['json_value_spans'][ptr+'/'+k],original_value=v) for k,v in obj.items()})
OUT.mkdir(exist_ok=False)
rows=[]
for eid,inv_ids,block_ids,source_scope,target_scope,need,note,issue in A['rows']:
    row=dict(id=eid,source_scope=source_scope,target_scope=target_scope,necessity_and_missing_impact=need,proposal=note,
        source_evidence=[dict(inventory_id=i,artifact=ref(P/'evaluation/eval-v1/inventory.json'),pointer=f'/items/{im[i][0]}',
            exact_child_evidence=im[i][1]['evidence'],gold_status='No new gold or owner acceptance inferred from inventory mapping.') for i in inv_ids.split(',') if i],
        bounded_independent_source=[blocks[k] for k in block_ids],target_source_actual=None,
        target_source_policy='Actual candidate target absent. Supplied chart descriptions/Step4 are partial related context, never substitute target content or establish aliases.',
        reviewer=A['reviewer'],authoring=ref(M/'annotations.json'),human_status='waiting_review',human_reviewer=None,
        separate_issue='SEM-017' if issue else None,runs={})
    vals=[]
    for run,prop in props.items():
        edge=next(x for x in prop['dependencies'] if x['id']==eid);assert edge['to'] is None
        vals.append(edge)
        source=C['output_records'][run][edge['from']]['original_record']
        ids=list(dict.fromkeys([eid,edge['from'],*edge['gap_ids'],*edge['evidence_ids'],*source.get('gap_ids',[]),*source.get('evidence_ids',[])]))
        supplemental=[step] if run=='context-01' and eid in ['D911shock','D923shock','D932CRT'] else []
        row['runs'][run]=dict(response=C['responses'][run],record_present=True,reviewer=A['reviewer'],human_reviewer=None,status='waiting_review',
            evaluator_compared=True,meaning_result='not_assessable',source_scope=source_scope,target_scope=target_scope,
            target_identity=dict(output_id=None,candidate=edge['target_candidate'],actual_target_content='not_supplied',alias_identity='not_assessable'),
            direction=dict(observed_from=edge['from'],observed_to=edge['target_candidate'],assessment='Using/modifying/qualifying source clause -> named required target; supported within exact authored scope, not external alias identity.'),
            kind=dict(observed=edge['kind'],assessment='supported_as_bounded_relation_role; absent target content not certified'),
            explicitness=dict(observed=edge['explicitness'],assessment='supported_in_bounded_scope',basis='ZOC definition dependency inferred from term in condition; other source names/numbers directly refer to used/modified/excepted target.'),
            necessity=need,missing_target_impact=dict(observed=edge['impact_if_missing'],evaluator_scope=need,
                full_dependent_result='blocked for missing applicable target content/qualifications',
                local_source_operator='Does not automatically block source-supplied exception/prohibition/modifier with supplied relevant facts.',
                classification='owner_scope_decision_required' if issue else 'supported_only_in_bounded_full_execution_scope'),
            output_trace={i:trace(run,i) for i in ids},supplemental_supplied_context=supplemental,
            comparison=note,proposed_assessment='separate_block_scope_decision' if issue else 'supported_named_requirement_and_relation_role',
            exclusions=['Whole source/target records and unreviewed fields','Actual absent target text, values, map/chart identity or alias equivalence',
                'Blanket blocking of source-supplied local operator/exception with given facts','All earlier pending scopes/remaining SEM-004',
                'Full combat/withdrawal/stacking outcomes, real ratings/setup,20situations','Locator/glyph review, newgold, final TP/FP/FN/precision/recall'],
            uncertainties=['Actual target content/qualifications absent', 'No new owner decision; pending is not TP or definite FP.'])
    row['output_values_identical_between_runs']=vals[0]==vals[1]
    row['run_difference_assessment']='Changed candidate/impact/evidence narrows remaining CRT need after supplied operators; no full closure or order acceptance.' if eid=='D932CRT' else 'No edge field change; context can still change related node/gap information.'
    rows.append(row)
assert sum(x['output_values_identical_between_runs'] for x in rows)==29
positive=[x['id'] for x in rows if not x['separate_issue']]
summary=dict(assigned_distinct_ids=30,assigned_occurrences=60,per_answer={'first-001':30,'context-01':30},
    evaluator_compared_occurrences=60,positive_bounded_ids=positive,positive_bounded_occurrences=52,separate_issue_ids=A['separate_issue_edge_ids'],separate_issue_occurrences=8,
    owner_available_occurrences=60,new_owner_reviewed_occurrences=0,owner_pending_occurrences=60,owner_actual_open_or_read='unknown',
    previous_owner_decided_assigned_scopes=125,total_evaluator_compared_assigned_occurrences=185,remaining_uncompared_occurrences=72,
    pending_expectation_ids=prior['pending_expectation_ids'],unconfirmed_candidates_not_gold=105,
    TP_gold='not_assessable',TP_output='not_assessable',FP='not_assessable',FN='not_assessable',precision='not_assessable',recall='not_assessable')
payload=dict(id='M-POC5A.4b2-comparisons-01',card='M-POC5A.4b2',status='partial_waiting_review',evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
    scope_plan=ref(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json'),estimate=ref(M/'start.json'),method=A['method'],
    source_span_policy='Manual exact clause scope precedes containing independent helper block and child inventory evidence; mapping does not confer acceptance.',
    source_images_inspected=[ref(P/f'inputs/v1/pages/pdf-{n}.png') for n in [31,32,33,34,37]]+[step['image']],
    summary=summary,relationships=rows,previous_state=ref(R/'current-state-11.json'),owner_decision=ref(R/'owner-decision-05.json'),
    owner_overlay=ref(R/'owner-review-overlay-05.json'),new_owner_decisions=[],inherited_issues=prior['unresolved_issue_ids'],
    limits=C['limits'],limitations=C['limitations'],other_parts_executed=False)
save(OUT/'comparisons.json',payload)
issue=copy.deepcopy(A['new_issue']);issue.update(status='waiting_review',scope=A['separate_issue_edge_ids'],occurrences=8,
    reviewer=A['reviewer'],human_reviewer=None,evaluation=C['evaluation'],responses=C['responses'],source=C['source'],
    comparison_packet=ref(OUT/'comparisons.json'),actual_wrong_played_outcome='not_demonstrated')
save(OUT/'issues.json',dict(issues=[issue],inherited_pending=prior['unresolved_issue_ids'],
    previous_dispositions_preserved=prior['issue_dispositions'],wrong_read='not_assessable',confirmed_semantic_error_counts='not_assessable',
    policy='SEM-017 is scoped ambiguity; not automatic FP. No previous issue or blocking full outcome closed.'))
presentation=dict(card='M-POC5A.4b2',positive_scope=dict(ids=positive,occurrences=52,per_answer={'first-001':26,'context-01':26},
    includes=['Exact source occurrence','Named target requirement, not actual absent target content or alias','Source-to-target direction, bounded relation kind and explicitness',
        'Necessity/block only for described full dependent execution; locally supplied operator with given facts remains separately supported'],
    excludes=rows[0]['runs']['first-001']['exclusions']),separate_issue=dict(id='SEM-017',ids=A['separate_issue_edge_ids'],occurrences=8),
    owner_available_occurrences=60,evaluator_compared_occurrences=60,new_owner_reviewed_occurrences=0,owner_pending_occurrences=60,
    actual_owner_file_open_or_read='unknown',proposal_only=True,next_after_owner_decision='Separate M-POC5A.4b3:36IDs/72occurrences; estimate before execution.')
save(OUT/'presentation.json',presentation)
lines=['# M-POC5A.4b2 — rzeczywiste porównania wszystkich 30 ID','',
    '60 wystąpień: 30 first-001 i 30 context-01. Recenzent propozycji: Codex; właściciel akceptuje znaczenie. Wszystkie nowe decyzje waiting_review.',
    '', '52 wystąpienia mają propozycję przyjęcia ograniczonej roli relacji/wymagania źródła. Dla 8 wydzielono osobną decyzję o zakresie blokady SEM-017. To nie liczba poprawnych całych rekordów lub TP.',
    '',*[f"{run}: `{a['sha256']}`, {a['bytes']} bajtów." for run,a in C['responses'].items()],
    '',f"eval-v1 `{C['evaluation']['sha256']}`; PDF `{C['source']['sha256']}`.",
    '', '[Pełne ślady obu wyników](comparisons.json) zawierają surowe rekordy i pola, źródła, pointers, zakresy bajtów [start,end) i hashe. Brakującego celu nie odczytano; nie jest zastąpiony nazwą/opisem modelu.', '']
for row in rows:
    lines += [f"## {row['id']}",'','Źródło i dokładny zakres: '+row['source_scope'],'','Cel i granica dostępności: '+row['target_scope'],
        '', 'Konieczność / zakres blokady: '+row['necessity_and_missing_impact'],'','Porównanie i propozycja: '+row['proposal'],'']
    for run,x in row['runs'].items():
        t=x['output_trace'][row['id']];e=t['original_record'];sp=t['raw_span']
        lines += [f"**{run}:** `{t['pointer']}`; bajty [{sp['start_byte']},{sp['end_byte_exclusive']}), SHA-256 `{sp['sha256']}`.",'',
            f"Zapis modelu: `{e['from']}→candidate`, `{e['kind']}/{e['explicitness']}`, `{e['target_status']}`, blocks_full_result=`{e['impact_if_missing']['blocks_full_result']}`.",'',
            'Dosłowny kandydat modelu (nie dostarczone źródło celu): '+json.dumps(e['target_candidate'],ensure_ascii=False),'',
            'Uzasadnienie modelu: '+e['rationale'],'', 'Deklaracja wpływu modelu: '+json.dumps(e['impact_if_missing'],ensure_ascii=False),'',
            'Ocena: '+x['proposed_assessment']+'. '+x['missing_target_impact']['evaluator_scope'],'']
        for gid in e['gap_ids']:
            g=x['output_trace'][gid]['original_record']
            lines += ['Zapis gapu modelu: '+gid+' — '+g['reason']+' Potrzebny kontekst: '+g['needed_context'],'']
    for b in row['bounded_independent_source']:
        lines += [f"Dostarczona niezależna transkrypcja: `{b['artifact']['path']}`, `{b['pointer']}`, znaki [{b['character_range'][0]},{b['character_range'][1]}), SHA-256 wycinka `{b['utf8_excerpt_sha256']}`. Dokładna oceniana klauzula to zakres powyżej, nie cała koperta.",'',
            '> '+b['literal_helper_text'].replace('\n','\n> '),'']
    if row['id'] in ['D911shock','D923shock','D932CRT']:
        lines += ['Dodatkowy wcześniej dostarczony kontekst tylko dla context-01: Step4. Nie dostarcza wcześniejszych etapów lub rzeczywistej CRT.','',
            '> '+step['literal_helper_text'].replace('\n','\n> '),'']
    lines += ['Wyłączenia: treść niepozyskanego celu, aliasy, całe rekordy/nieprzejrzane pola, blanket blocking lokalnych operatorów, wcześniejsze pending, pełne wyniki/realny setup, lokatory,20sytuacji i metryki.','']
lines += ['## Granice wyniku','',
    '29 krawędzi identycznych, D932CRT zmieniona; dodatkowo G-D923shock i G-D932CRT zawężono po kontekście. Brak nowych źródeł lub korekt. ',
    'Właścicielowi udostępniono60; oceniający porównał60; nowych decyzji właściciela0; pending60. Faktyczny odczyt/otwarcieunknown.',
    'Poprzednie125 zakresów mają własne decyzje; razem185 przypisanych wystąpień porównano. .4b3 ma72 niewykonane jako pełna partia, z wcześniej rozstrzygniętym tylko dodatkowym wystąpieniem D961stack.',
    'SEM-001–013 zachowane w nierozstrzygniętych zakresach, w tym resztaSEM-004. DecyzjeSEM-014–016 zachowane, nie rozszerzone. Osiem oczekiwań nadalpending. 105 candidates nie staje sięgold. PełneTP/FP/FN/precision/recall not_assessable.',
    '1 dodatkowa strona/1reguła/0tabel,1runda/0korekt;0pełnych domknięć,4częściowe aktualizacje i4nowe deklaracje. Trzeciego źródła nie pozyskano. Izolacja ścieżek naruszona w dawnym context-01, odczyt oceny niezaobserwowany; ekspozycja/czysty kontekst/aktywny budżet unknown.',
    'Następny krok: decyzje dla owner-focus, potem osobna .4b3 po oszacowaniu. M-POC5A/.4/.4b partial; M-POC5 jedyny next.','']
(OUT/'comparisons.md').write_text('\n'.join(lines),encoding='utf-8')
(OUT/'review.md').write_text('# M-POC5A.4b2 — przegląd wykonany\n\n'+A['method']+'\n\n'+
    'Przypisane30ID/60wystąpień porównano, bez brakującego ID. 52 ograniczone pozytywne propozycje,8 z osobną kwestiąSEM-017; wszystkiewaiting_review. '+
    '29edges identycznych;D932CRT i2gapy wymagają odrębnego porównania kontekstu.\n\n'+
    '[Każde porównanie](comparisons.md), [ślad JSON](comparisons.json), [decyzje po ludzku](owner-focus.md), [kwestie](issues.json).\n\n'+
    '\n\n'.join(lines[-9:]),encoding='utf-8')
save(M/'packet-summary.json',summary)
print(json.dumps(summary,ensure_ascii=False))
