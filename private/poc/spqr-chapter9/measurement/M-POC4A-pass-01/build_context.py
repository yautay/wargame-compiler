"""Materialize one bounded context package, with evaluator-only evidence separated."""
import collections
import datetime
import re
from PIL import Image
from prepare import ROOT,P,M,load,desc,save

C=P/'context/pass-01'
assert not C.exists(), 'New pass required; never overwrite a prior pass'
budget=load(M/'pre-expansion-budget.json')
assert budget['counts']['pages']==1 and budget['counts']['rules']==1
assert budget['counts']['longest_considered_path_depth']==2
index=load(M/'source-locator-index.json')['rule_heading_candidates']
loc=load(M/'selected-source-locator.json')
proposal=load(P/'proposals/first-001/proposal.json')
prov=load(P/'proposals/first-001/provenance.json')
evaldeps=load(P/'evaluation/eval-v1/dependencies.json')
exps=load(P/'evaluation/eval-v1/expectations.json')['expectations']
sits=load(P/'evaluation/eval-v1/situations.json')['situations']
draft=load(P/'evaluation/draft/dependencies.json')['dependencies']
inventory=load(P/'evaluation/eval-v1/inventory.json')
print('inventory keys',list(inventory))

def candidates(label):
    result=[]
    for num in dict.fromkeys(re.findall(r'\b\d{1,2}\.\d{1,2}\b',label)):
        for hit in index.get(num,[]):result.append(dict(rule=num,**hit))
    return result

# Named procedures are lookup candidates, never new accepted aliases or execution edges.
procedure_map=[('pre-shock','8.43'),('reaction fire','8.2'),('orderly withdrawal','6.5'),
    ('harassment','8.3'),('h&d','8.3'),('superiority','8.46'),('shock resolution','8.4'),
    ('line command','4.3'),('individual order','5.2'),('column','6.7'),('line of sight','8.14'),
    ('los','8.14'),('rout point','11.1'),('momentum','5.3'),('recovery','10.16'),
    ('cohesion hit recovery','10.16'),('deplet','10.3'),('stacking','6.6'),('zoc','7.2'),
    ('facing','7.1'),('orders phase','5.2'),('game turn','3.0'),('missile supply','8.17'),
    ('missile fire','8.1'),('movement mp','6.1'),('repeat movement','6.13')]
def source_lookup(label):
    lower=label.lower()
    exact=candidates(label)
    # A named chart's rulebook reference does not supply its rows/notes.
    if any(t in lower for t in ['mrrc','missile range','combat table','shock crt','shock combat results',
            'shock combat crt','clash of spears','shock superiority chart','stacking chart',
            'movement cost chart','cohesion hit and tq check chart']):
        return dict(status='blocked_source',reason='Exact table with rows, headers and notes not supplied in the verified bounded source set. Rulebook references are not the table; absence from the whole game is not asserted.',
            locator_candidates=exact,scope='Exact named chart/row only; no alias equivalence accepted')
    if any(t in lower for t in ['scenario','battle-specific','battle map','map compass','actual selected battle',
            'assigned leader','initiative rating','eligible li','army withdrawal level','current roman rout points',
            'roman/ala/allied line identity','specific command restrictions','counter tq','counter ma']):
        return dict(status='blocked_source',reason='Concrete battle/scenario/unit identity and matching map/setup/rating/state evidence not supplied. Generic rulebook and synthetic examples cannot establish it.',
            locator_candidates=exact,scope='One identified scenario/map/unit and the requested parameter')
    if exact:
        return dict(status='source_locator_candidate_deferred',reason='Rule heading located in hash-verified PDF. Exact needed clause/procedure completeness and necessity remain pending; not selected for full execution.',
            locator_candidates=exact,scope=label)
    for phrase,rule in procedure_map:
        if phrase in lower and candidates(rule):
            return dict(status='source_locator_candidate_deferred',reason='Named-procedure lookup candidate in verified PDF; not an accepted alias, meaning or complete dependency closure.',
                locator_candidates=candidates(rule),scope=label)
    return dict(status='blocked_source',reason='Exact target identity/scope unresolved in the bounded lookup; no source is invented and no broad instruction acquisition authorized by this candidate.',
        locator_candidates=[],scope=label)

def effect(situation_ids):
    rows=[]
    for sid in situation_ids:
        s=next(x for x in sits if x['id']==sid)
        rows.append(dict(id=sid,frozen_kind=s['expected']['kind'],impact=
            'Concrete source gap continues expected block; no outcome generated.' if s['expected']['kind']=='justified_block'
            else 'Frozen local result uses supplied/synthetic facts. External lookup does not silently replace it with full real-state execution; semantic result remains not_assessable.'))
    return rows or [dict(id=None,impact='No linked frozen situation; full real-state execution in this scope remains unavailable/pending, without changing the 20-situation denominator.')]

internal=[]
for d in evaldeps['confirmed_execution_relations']:
    evidence=d.get('evidence',[]) + ([d['source_evidence']] if d.get('source_evidence') else [])
    # Source/target mapping is retained from the frozen bounded relation only.
    parent=next((x for x in draft if x['id']==d['id']),{})
    internal.append(dict(id=d['id'],from_id=d['from'],to_id=d['to'],criticality=d['criticality'],
        status='source_already_in_baseline',source_id='SPQR-5E-ch9-source-v1',
        source_sha256=load(P/'source/source-v1.json')['source']['sha256'],
        baseline_input_manifest=desc(P/'inputs/v1/manifest.json'),evidence=evidence,
        source_scope=d.get('necessity_scope',d.get('scoring_scope')),
        situation_impacts=effect(parent.get('situation_ids',[])),
        delta=dict(pages=0,rules=0,tables=0),
        relation_observation='Structural omission in first-001; new external source not justified.' if d['id'].startswith('DEP-NEW') else 'Tuple candidate only; semantic match pending.',
        new_human_acceptance='not_performed'))

critical_context=[]
for exp in exps:
    if exp.get('classification')!='requires_context':continue
    key=exp['id']
    lookup=source_lookup(' '.join(exp.get('limits',[])))
    if key=='EXP-031':
        lookup=dict(status='partial_source_selected',reason='Only numerical procedure 8.46 Step 4 selected. Exact Shock CRT missing; AS/LC order remains human review, no resolved interpretation.',locator_candidates=candidates('8.46'),scope='8.46 Step 4 plus blocked exact Shock CRT',blocked_target='CTX-TBL-SHOCK-CRT')
    elif key=='EXP-074':lookup=source_lookup('actual counter TQ/MA; identified unit required')
    critical_context.append(dict(id='CTX-'+key,expectation_id=key,criticality=exp['criticality'],
        human_decision_scope=exp['reviewed_scope'],source_lookup=lookup,
        situation_impacts=effect(exp['parent_situation_ids']),status=lookup['status'],
        new_source_acceptance='waiting_review',semantic_result='not_assessable'))

candidate_relations=[]
for d in draft:
    if d['id'] not in {x['id'] for x in evaldeps['unconfirmed_execution_candidates']}:continue
    target=d.get('target_candidate') or {}
    label=' '.join(str(target.get(k,'')) for k in ['identifier','name','facet'])
    lookup=source_lookup(label)
    candidate_relations.append(dict(id=d['id'],criticality_declaration=d.get('criticality','unknown'),
        criticality_status='unconfirmed_parent_declaration; not new gold',target_candidate=target,
        source_lookup=lookup,situation_impacts=effect(d.get('situation_ids',[])),
        necessity_review='pending',selected=False,scope=d.get('necessity_scope','unconfirmed'),
        reason_not_selected='Unconfirmed candidate does not itself justify adding broad context for full execution. Source location and necessity are separate.'))
assert len(candidate_relations)==105

gap_rows=[]
deps_by_id={d['id']:d for d in proposal['dependencies']}
evidence_by_id={e['id']:e for e in proposal['evidence']}
errors=load(P/'reports/first-001/errors.json')['errors']
for i,g in enumerate(proposal['gaps']):
    if g['class']!='missing_context':continue
    ref=next((deps_by_id[a].get('target_candidate') for a in g['affected_ids'] if a in deps_by_id),None) or {}
    label=ref.get('original_reference',g['needed_context'])
    lookup=source_lookup(label+' '+g['needed_context'])
    chosen=g['id'] in ['G932','G-D932CRT','G-D962shock']
    if chosen:
        lookup=dict(status='partial_source_selected',reason='Selected exact 8.46 Step 4 procedure only; required CRT/other steps remain blocked or deferred. No semantic fix asserted.',locator_candidates=candidates('8.46'),scope='8.46 Step 4 only',blocked_target='CTX-TBL-SHOCK-CRT')
    rule_numbers={re.sub(r'[^0-9]','',a)[0:3] for a in g['affected_ids'] if a.startswith('R')}
    linked=[s['id'] for s in sits if any(re.sub(r'[^0-9]','',r)[0:3] in rule_numbers for r in s.get('inventory_refs',[]) if r.startswith(('R-','C-')))]
    observations=[]
    for eid in g['evidence_ids']:
        e=evidence_by_id[eid]
        observations.append(dict(id=eid,source={k:e[k] for k in ['source_id','source_sha256','pdf_page','region_id']},quote=e.get('quote'),
            status='Baseline evidence binding retained; cited occurrence is not proof that external context is necessary.'))
    gap_rows.append(dict(id=g['id'],response_pointer='/gaps/'+str(i),raw_span=prov['json_value_spans']['/gaps/'+str(i)],
        baseline_error_ids=[e['id'] for e in errors if '/gaps/'+str(i) in e.get('response_pointers',[])],
        extractor_declaration=g,independent_necessity='pending',criticality='unknown',
        source_occurrence=observations,source_lookup=lookup,situation_impacts=effect(linked),
        selection='selected_partial' if chosen else 'not_selected',
        scope_reason='Only a confirmed context requirement or a bounded supporting component is acquired; local synthetic conclusions and internal omissions do not require automatic external expansion.'))
assert len(gap_rows)==79

# Budget was written before this directory and its source artifacts existed.
C.mkdir(parents=True)
(C/'evidence').mkdir()
image=Image.open(M/'pdf-27.png')
sx=image.width/612;sy=image.height/792
pixel_box=[round(40*sx),round(413*sy),round(300*sx),round(650*sy)]
image.crop(pixel_box).save(C/'evidence/8.46-step-4-pdf-27.png')
(C/'evidence/8.46-step-4-helper.txt').write_text(loc['helper_text']+'\n',encoding='utf-8')
save(C/'evidence/8.46-step-4-scope.json',dict(id='CTX-RULE-8.46-S4',source=desc(P/'source/source-v1.json'),
    verified_pdf=desc(P/'source/original-pdf-20261008-01.pdf'),pdf_page=27,column='left',
    bbox_pdf_points=[40,413,300,650],pixel_bbox_on_reviewer_render=pixel_box,
    full_render=desc(M/'pdf-27.png'),rule='8.46',fragment='Step 4: Apply Results',
    parent_heading_page=26,scope='All four Step 4 bullets and final distribution cross-reference; no base table, Step 1-3, or 8.47 supplied.',
    reason='Bounded numerical procedure sought by existing gap; no new values, lookup or interpretation.',
    source_visual_check='Codex viewed full PDF 26 and 27 renders, confirmed heading lineage and complete Step 4 scope; crop review follows.',
    human_review='waiting_review',meaning_acceptance='not_performed'))
save(C/'declaration-review.json',dict(id='M-POC4A-79-declarations',parent_errors=desc(P/'reports/first-001/errors.json'),
    parent_proposal=desc(P/'proposals/first-001/proposal.json'),count=79,rows=gap_rows,
    ambiguity_declarations=[g for g in proposal['gaps'] if g['class']!='missing_context'],
    ambiguity_policy='G916/G953 go to M-POC5 review against frozen scopes; do not obtain invented clarifications or change baseline.',
    classification_counts=dict(collections.Counter(r['source_lookup']['status'] for r in gap_rows))))
save(C/'critical-source-audit.json',dict(confirmed_execution_count=8,confirmed_execution=internal,
    frozen_context_requirements_count=8,frozen_context_requirements=critical_context,
    unconfirmed_candidate_count=105,unconfirmed_candidates=candidate_relations,
    critical_candidate_declarations=sum(x['criticality_declaration']=='critical' for x in candidate_relations),
    candidate_policy='Parent criticality is reported as a declaration. Neither lookup candidates nor earlier model flags confer accepted criticality, aliases or source acceptance.',
    denominator=20,situation_results='not_assessable',human_review='waiting_review'))
targets=dict(id='M-POC4A-pass-01',status='prepared_waiting_review',card_outcome='partial',
    parent_run='first-001',parent_response=desc(P/'runs/first-001/first-001.json'),
    baseline_closure=desc(P/'reports/first-001/closure.json'),evaluation_id='eval-v1',
    evaluation_manifest=desc(P/'evaluation/eval-v1/manifest.json'),source=desc(P/'source/source-v1.json'),
    budget_before_expansion=desc(M/'pre-expansion-budget.json'),budget=budget,
    selected=[dict(id='CTX-RULE-8.46-S4',rule='8.46',scope='Step 4 only, PDF27 left [40,413,300,650]',
        reason='EXP-031 context requirement; G932/G-D932CRT and shared G-D962shock procedure component.',
        path=['9.32','8.46/Step-4'],depth=1,delta=dict(unique_pages=[27],unique_rules=['8.46'],unique_tables=[]),
        affected_situations=['SIT-09','SIT-13'],
        impact='Source component supplied; synthetic local outputs unchanged; real AS/CRT case still blocked and human interpretation pending.',
        source_status='located_visually_by_codex',human_acceptance='waiting_review')],
    blocked=[dict(id='CTX-TBL-SHOCK-CRT',name='Shock CRT',status='blocked_source',path=['9.32','8.46/Step-4','CTX-TBL-SHOCK-CRT'],depth=2,
        reason='Exact table rows/headers/notes not supplied; references do not establish the actual table. No lookup values invented.',
        impact='Real base-result/AS lookup remains unavailable. SIT-09 supplied unadjusted result and local result retain frozen scope; no blanket new block.')],
    source_audit=desc(C/'critical-source-audit.json'),declarations_audit=desc(C/'declaration-review.json'),
    table_and_unnumbered_id_policy='CTX-TBL-SHOCK-CRT names the blocked chart; CTX-EXP-010/019/033/050/064/066/074 name exact unnumbered context requests.',
    review_gate='Critical sources and interpretation require human review before package freeze/transfer; no human approval recorded.',
    time_compliance='unknown',new_inference_responses=0,new_corrective_responses=0,
    planned_context_response_round=1,performed_context_response_rounds=0,semantic_result='not_assessable')
save(C/'targets.json',targets)
print('Prepared',len(gap_rows),'declarations;',len(internal),'confirmed;',len(candidate_relations),'candidates')
print('Declaration source states:',dict(collections.Counter(r['source_lookup']['status'] for r in gap_rows)))
