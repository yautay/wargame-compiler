"""Initial one-session authoring aid for manually selected ranges; no runtime pipeline.

Final draft separates the hypothesized MRRC target of9.13 from explicit named
references, and distinguishes explicit unnumbered terms from implicit hypotheses.
That subsequent authoring adjustment is recorded in the final candidate JSON.
This captured aid refuses to overwrite outputs; it is not a regeneration command.
"""
from pathlib import Path
import json, hashlib, re
from collections import Counter
import pdfplumber

ROOT = Path('C:/dev/wargame-compiler')
P = ROOT / 'private/poc/spqr-chapter9'
E = P / 'source/review-evidence'
SRC = Path('C:/dev/spqr/sources/SPQR+Deluxe_Rule+book_WEB.pdf')
SOURCE_ID = 'SPQR-5E-ch9-source-v1'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def save(p,obj):
    assert not p.exists(), f'Refusing overwrite: {p}'
    p.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

lines = {}
with pdfplumber.open(SRC) as doc:
    for n in range(31,38):
        for c,box in [('L',(40,45,305,744)),('R',(305,45,573,744))]:
            rows=doc.pages[n-1].crop(box).extract_text_lines(x_tolerance=2,y_tolerance=3,return_chars=False)
            expected=(E/f'pdf-{n}-{"left" if c=="L" else "right"}.txt').read_text(encoding='utf-8').splitlines()
            assert [r['text'] for r in rows]==expected
            lines[(n,c)]=rows

def evidence(spec):
    # Explicitly authored one-based helper-line ranges, in logical column order.
    result=[]
    for token in spec.split(';'):
        m=re.fullmatch(r'(\d+)([LR]):(\d+)-(\d+)',token)
        n,c,a,b=m.groups(); n,a,b=int(n),int(a),int(b)
        rows=lines[(n,c)][a-1:b]
        result.append({'source_id':SOURCE_ID,'source_sha256':sha(SRC),
          'pdf_page':n,'printed_page':str(n),'column':'left' if c=='L' else 'right',
          'render':f'source/review-evidence/pdf-{n}.png','render_sha256':sha(E/f'pdf-{n}.png'),
          'bbox_pdf_points':[round(min(r['x0'] for r in rows),3),round(min(r['top'] for r in rows),3),round(max(r['x1'] for r in rows),3),round(max(r['bottom'] for r in rows),3)],
          'bbox_precision':'text-line envelope; does not include adjacent counter artwork',
          'helper_file':f'source/review-evidence/pdf-{n}-{"left" if c=="L" else "right"}.txt',
          'helper_lines_inclusive':[a,b],'transcription':'\n'.join(r['text'] for r in rows),
          'reading_status':'visually_checked_by_codex','human_review':'pending'})
    return result

items=[]
def add(id,typ,parent,spec,label=None,classification='text_unit',review=[]):
    row={'id':id,'type':typ,'parent_id':parent,'original_label':label,
         'classification':classification,'evidence':evidence(spec),
         'observation_status':'visually_checked_by_codex','human_review':'pending',
         'semantic_acceptance':'not_performed','review_issue_ids':review}
    items.append(row); return row

headings=[('9.0','31R:19-19'),('9.1','31R:20-20'),('9.2','33R:1-2'),('9.3','34L:8-8'),('9.4','34L:18-18'),('9.5','34R:1-1'),('9.6','35L:1-1'),('9.7','35R:24-24'),('9.8','36L:1-1'),('9.9','36L:44-44')]
for label,spec in headings: add('H-'+label,'chapter_heading' if label=='9.0' else 'section_heading',None if label=='9.0' else 'H-9.0',spec,label,'heading')

# Each pipe-separated range below is a manually selected paragraph, bullet, step,
# sentence cluster or table-trigger block, not a claim of atomic semantic gold.
RULES = '''
9.11|31R:31-37;31R:38-38;31R:39-39;31R:40-41;31R:42-44;31R:45-45;31R:46-47;31R:48-50;32L:1-4;32L:5-8
9.12|32L:14-19;32L:20-21;32L:22-24
9.13|32L:25-28
9.14|32L:32-35;32R:10-12;32R:16-24;32R:25-29;32R:30-30;32R:31-31;32R:32-32;32R:33-34;32R:35-36;32R:37-42;32R:43-44+33L:1-2
9.15|33L:7-15
9.16|33L:16-25
9.17|33L:26-29
9.18|33L:31-32
9.19|33L:33-37
9.21|33R:15-21
9.22|33R:22-25
9.23|33R:26-27;33R:28-28;33R:29-31;33R:32-34;33R:35-36;33R:37-42
9.24|33R:46-46;33R:47-47;33R:48-48;33R:49-51;33R:52-53+34L:1-1
9.31|34L:9-11
9.32|34L:12-14
9.41|34L:19-28
9.51|34R:6-15
9.52|34R:16-17;34R:18-18;34R:19-21;34R:22-25;34R:26-28;34R:29-30
9.53|34R:31-32;34R:33-33;34R:34-36;34R:37-38;34R:39-40;34R:41-43;34R:44-47;34R:48-50
9.61|35L:10-18
9.62|35L:19-25
9.63|35L:26-28
9.64|35L:29-33
9.65|35L:34-35
9.66|35L:38-42+35R:1-6
9.67|35R:7-14
9.68|35R:19-23
9.71|35R:31-32;35R:33-35;35R:36-38
9.72|35R:39-43
9.81|36L:2-7
9.82|36L:8-16
9.83|36L:19-20
9.84|36L:21-23
9.85|36L:24-33
9.86|36L:34-41
9.87|36L:42-43
9.91|36L:48-48;36L:49-51+36R:1-2
9.93|36R:3-3;36R:4-4;36R:5-5
9.94|36R:6-6;36R:13-16;36R:17-24
9.95|36R:25-25;36R:26-34
9.96|36R:35-35;36R:44-49;36R:50-52+37L:1-14;37L:15-16;37L:17-19;37L:20-21;37L:22-26
'''
for raw in RULES.strip().splitlines():
    label,ranges=raw.split('|'); groups=ranges.split(';')
    # Parent evidence is union of child source fragments, not an extra denominator.
    full=';'.join(g.replace('+',';') for g in groups)
    row=add('R-'+label,'rule_label','H-'+label[:3],full,label,'numbered_rule', ['U-02'] if label=='9.96' else [])
    for i,g in enumerate(groups,1):
        evspec=g.replace('+',';')
        tx=' '.join(x['transcription'] for x in evidence(evspec))
        classification='list_item' if tx.startswith('•') else 'numbered_step' if re.match(r'^[1-4]\. ',tx) else 'paragraph_or_sentence_cluster'
        if (label,i) in [('9.11',6),('9.14',5),('9.23',1),('9.24',1),('9.52',1),('9.53',1),('9.71',1),('9.91',1),('9.93',1),('9.94',1),('9.95',1),('9.96',1),('9.96',4)]: classification='heading_or_list_introduction'
        add(f'C-{label}-{i:02}','clause_group','R-'+label,evspec,None,classification,['U-01'])

# The applicability paragraph under 9.7 is operative content without its own rule label.
add('C-9.7-01','clause_group','H-9.7','35R:25-30',None,'unnumbered_applicability_paragraph',['U-01','U-07'])

NOTES=[('N-01','H-9.1','31R:21-30','historical'),('N-02','R-9.11','32L:9-13','design'),('N-03','R-9.13','32L:29-31','design'),('N-04','R-9.14','33L:3-6','design'),('N-05','R-9.17','33L:30-30','historical'),('N-06','R-9.19','33L:38-52','historical'),('N-07','H-9.2','33R:3-14','design'),('N-08','R-9.41','34L:34-39','design'),('N-09','H-9.5','34R:2-5','design'),('N-10','H-9.6','35L:2-9','historical'),('N-11','R-9.82','36L:17-18','play'),('N-12','H-9.9','36L:45-47','design'),('N-13','R-9.94','36R:7-12','design'),('N-14','R-9.96','36R:36-43','design')]
for id,parent,spec,kind in NOTES: add(id,'note',parent,spec,None,kind+'_note',['U-02'] if id=='N-14' else ['U-03'] if id in ['N-03','N-07','N-09'] else [])
EXAMPLES=[('X-01','R-9.14','32R:13-15'),('X-02','R-9.23','33R:43-45'),('X-03','R-9.24','34L:2-7'),('X-04','R-9.32','34L:15-17'),('X-05','R-9.41','34L:29-33'),('X-06','R-9.53','34R:51-51'),('X-07','R-9.67','35R:15-18')]
for id,parent,spec in EXAMPLES: add(id,'caption' if id=='X-01' else 'example',parent,spec,None,'illustrative_example',['U-04'] if id=='X-01' else [])

t=add('T-01','table','R-9.14','32L:36-45;32R:1-9',None,'die_roll_result_table',['U-04'])
t['columns']=['Die Roll','Result'];t['observed_row_labels']=['0','1–6','7–9'];t['fragment_order']=['left header and rows 0, 1–6','right row 7–9 without repeated header']
for id,spec,label in [('TR-01','32L:37-40','0'),('TR-02','32L:41-45','1–6'),('TR-03','32R:1-9','7–9')]: add(id,'table_row','T-01',spec,label,'observed_table_row',['U-04'])

def graphic(id,typ,parent,page,col,bbox,description,issue=[]):
    items.append({'id':id,'type':typ,'parent_id':parent,'original_label':None,'description':description,
      'evidence':[{'source_id':SOURCE_ID,'source_sha256':sha(SRC),'pdf_page':page,'printed_page':str(page),'column':col,
      'render':f'source/review-evidence/pdf-{page}.png','render_sha256':sha(E/f'pdf-{page}.png'),'bbox_pdf_points':bbox,
      'bbox_precision':'manually inspected approximate graphic envelope'}],
      'observation_status':'visually_checked_by_codex','human_review':'pending','semantic_acceptance':'not_performed','review_issue_ids':issue})
graphic('D-01','diagram','R-9.14',32,'right',[350,220,535,299],'Two elephant counters/hexes, orientation compass labels 1–6; X-01 is the accompanying example caption.',['U-04'])
graphic('D-02','diagram','R-9.66',35,'left',[80,516,266,665],'Two stacks and red arrows above four unstacked counters/hexes; two separate panel captions.',['U-05'])
add('CAP-01','caption','D-02','35L:36-36',None,'panel_caption',['U-05'])
add('CAP-02','caption','D-02','35L:37-37',None,'panel_caption',['U-05'])
for args in [('G-01','counter_illustration','R-9.11',31,'right',[315,482,352,521],'Elephant counter adjacent to 9.11.'),('G-02','counter_illustration','R-9.21',33,'right',[315,239,352,276],'Skirmisher counter adjacent to 9.21.'),('G-03','counter_illustration','R-9.81',36,'left',[45,71,82,109],'Scorpio counter adjacent to 9.81.'),('G-04','marker_illustration','R-9.85',36,'left',[45,365,120,404],'Active Fire Once and Finished marker faces.'),('G-05','marker_illustration','R-9.86',36,'left',[260,528,297,566],'Reaction Fire Once marker face; Finished face is text only here.')]: graphic(*args)

CONT=[('K-01','C-9.11-08','C-9.11-09','31R:48-50','32L:1-4','procedure step 2 → step 3, same rule across pages'),('K-02','TR-02','TR-03','32L:41-45','32R:1-9','same table, left → right columns'),('K-03','C-9.14-11','C-9.14-11','32R:43-44','33L:1-2','same paragraph, page break'),('K-04','C-9.24-05','C-9.24-05','33R:52-53','34L:1-1','same bullet, page break'),('K-05','C-9.66-01','C-9.66-01','35L:38-42','35R:1-6','same paragraph, left → right columns'),('K-06','C-9.91-02','C-9.91-02','36L:49-51','36R:1-2','same paragraph, left → right columns'),('K-07','C-9.96-03','C-9.96-03','36R:50-52','37L:1-14','same paragraph, page break; continues to bullets before 10.0')]
for id,f,t,a,b,desc in CONT:
    row=add(id,'continuation','R-'+f.split('-')[1] if not f.startswith('TR') else 'T-01',a+';'+b,None,'physical_continuation')
    row.update({'from_item':f,'to_item':t,'from_fragment':evidence(a),'to_fragment':evidence(b),'direction_reason':desc,'edge_is_semantic_gold':False})

issues=[
 {'id':'U-01','status':'waiting_review','kind':'segmentation','items':'all clause_group records','question':'Confirm paragraph/list-item clusters and decide where multi-sentence clusters need separate clause IDs. Introductory list text is counted separately and is not an independent norm.','context_needed':False},
 {'id':'U-02','status':'waiting_review','kind':'mixed_note_and_rule','items':['N-14','R-9.96'],'question':'The DESIGN NOTE contains an imperative to ignore Chariot references on Combat Tables. Confirm its operative scope separately from historical explanation.','context_needed':True},
 {'id':'U-03','status':'waiting_review','kind':'mixed_note_and_rule','items':['N-03','N-07','N-09'],'question':'Notes also contain statements about applicability, unit classification or scenario eligibility. Confirm which spans enter later expectations; do not discard solely by note color.','context_needed':True},
 {'id':'U-04','status':'waiting_review','kind':'table_and_graphic','items':['T-01','TR-01','TR-02','TR-03','D-01','X-01'],'question':'Review left/right table merge, first versus subsequent roll wording, Leader Elephant clause and compass vertex versus hexside. Figure uses example compass; battle map is still required.','context_needed':True},
 {'id':'U-05','status':'waiting_review','kind':'diagram_and_continuation','items':['D-02','CAP-01','CAP-02','K-05'],'question':'Confirm captions/panel correspondence and 9.66 column continuation. The diagram precedes the rule label; associate by explicit source reference.','context_needed':False},
 {'id':'U-06','status':'requires_context','kind':'external_targets','items':'all external/unresolved dependency candidates','question':'Confirm target identifiers, applicability, direction and relation type using required context later. Historical 19 references are not a verified graph.','context_needed':True},
 {'id':'U-07','status':'requires_context','kind':'scenario_scope','items':['C-9.7-01','R-9.94','R-9.95','R-9.96','N-09','X-06'],'question':'Scenario eligibility, commander identity, army withdrawal level, battle map and setup are outside verified chapter inventory. Confirm only the inventory scope now.','context_needed':True},
 {'id':'U-08','status':'waiting_review','kind':'boundaries_and_numbering','items':['H-9.0','K-07'],'question':'Confirm start PDF31 right, end PDF37 left before10.0, context exclusions and observed absence of9.92; do not synthesize a missing rule.','context_needed':False},
 {'id':'U-09','status':'waiting_review','kind':'auxiliary_transcription','items':['R-9.96','D-01','D-02','G-01','G-02','G-03','G-04','G-05'],'question':'Helper text has line-end hyphenation and small-cap artifacts. Graphic envelopes are approximate; embedded counter glyphs are not exhaustively transcribed. Use renders as authoritative evidence.','context_needed':False},
]

coverage=[]
for n,c,a,b,desc in [(31,'R',19,50,'chapter start, 9.1 and 9.11 steps1–2'),(32,'L',1,45,'9.11 continuation; 9.12–9.14; table start'),(32,'R',1,44,'table end; rampage diagram/caption and rule continuation'),(33,'L',1,52,'9.14 continuation;9.15–9.19 and notes'),(33,'R',1,53,'9.2;9.21–9.24 with final bullet continued'),(34,'L',1,39,'9.24 completion;9.3–9.4'),(34,'R',1,51,'9.5;9.51–9.53'),(35,'L',1,42,'9.6;9.61–9.66; MLE diagram'),(35,'R',1,43,'9.66 continuation;9.67–9.72, including unnumbered9.7 scope'),(36,'L',1,51,'9.8–9.9;9.81–9.91'),(36,'R',1,52,'9.91 continuation;9.93–9.96'),(37,'L',1,26,'9.96 completion before10.0')]:
    ids=[i['id'] for i in items if i['type'] not in ['rule_label','continuation'] and any(e['pdf_page']==n and e['column']==('left' if c=='L' else 'right') for e in i['evidence'])]
    claimed=set()
    for i in items:
        if i['type'] in ['rule_label','continuation']: continue
        for e in i['evidence']:
            if e['pdf_page']==n and e['column']==('left' if c=='L' else 'right') and 'helper_lines_inclusive' in e:
                x,y=e['helper_lines_inclusive']; claimed.update(range(x,y+1))
    assert set(range(a,b+1))<=claimed, (n,c,set(range(a,b+1))-claimed)
    coverage.append({'id':f'A-{n}-{c}','description':desc,'evidence':evidence(f'{n}{c}:{a}-{b}'),'item_ids':ids,'text_line_coverage':'all selected core lines assigned','graphics_review':'complete visual pass; graphic glyph transcription not exhaustive','human_review':'pending'})

inventory={'artifact':'M-POC1A-manual-inventory-draft','version':'draft-v1','source_id':SOURCE_ID,'source_sha256':sha(SRC),'assessment_version':'draft_unfrozen','created_date':'2026-10-07','author':'Codex manual session','method':'Full Poppler renders inspected manually; manually chosen helper-line ranges supply locations/transcriptions. No semantic extraction run.','coordinate_system':{'unit':'PDF points','origin':'top-left','axes':'x right, y down','page_size':[612,792],'render_scale':150/72},'clause_policy':'Provisional physical text clusters; not atomic executable rules. Parent labels and clusters are separate counts; no semantic coverage denominator or gold is established.','counts':dict(Counter(i['type'] for i in items)),'items':items,'areas':coverage,'uncertainties':issues,'numbering_observation':{'observed_rule_labels':[r.split('|')[0] for r in RULES.strip().splitlines()],'9.92':'not observed on rendered source between9.91 and9.93; not invented','historical_label_candidates':'50 match observed labels excluding chapter heading9.0; candidates rechecked against renders'},'review':{'status':'waiting_review','reviewer':None,'date':None,'owner_approval':False},'excluded_context':[{'pdf_page':31,'regions':['entire left column','right column before9.0'],'reason':'chapter8 context; no core labels or candidate occurrences counted'},{'pdf_page':37,'regions':['left column from10.0 onward','entire right column'],'reason':'chapter10 context; target10.13 visible here but outside chapter9'}]}
save(P/'evaluation/draft/inventory.json',inventory)

# Candidate occurrences: harvest the explicit reference tokens from manually
# selected units; manual review of their source was performed in this session.
candidates=[]
unit_items=[i for i in items if i['type'] in ['clause_group','note','example','caption','table_row']]
by_id={i['id']:i for i in items}
def candidate(from_id,target,category,kind,quote,ev,status='unresolved',why='Source-bearing rule uses or mentions the candidate target; relation kind remains provisional.'):
    id=f'DC-{len(candidates)+1:03}'
    candidates.append({'id':id,'from':from_id,'from_rule_or_section':by_id[from_id]['parent_id'],'to':None,'target_candidate':target,'category':category,'explicitness':'explicit' if category in ['numeric','named','continuation'] else 'implicit_candidate','proposed_kind':kind,'kind_status':'unreviewed_proposal','direction_reason':why,'evidence':ev,'anchor':quote,'observation_status':'visually_checked_by_codex','target_status':status,'human_review':'pending','verified_graph_edge':False,'criticality':'not_assessed_M-POC1A','missing_target_effect':'not yet evaluated; may block later expectation/situation; never guess'})
for i in unit_items:
    tx='\n'.join(e['transcription'] for e in i['evidence'])
    label=by_id.get(i['parent_id'],{}).get('original_label')
    for ref in dict.fromkeys(re.findall(r'(?<!\d)(?:[4-9]|10)\.\d{1,2}(?!\d)',tx)):
        if ref==label or (i['id']=='C-9.7-01' and ref=='9.7'): continue
        target={'identifier':ref,'source':'same_pdf','location':'unknown'}
        status='internal_label_observed' if 'R-'+ref in by_id else 'external_unresolved'
        if status=='internal_label_observed': target['inventory_id']='R-'+ref
        if ref=='10.13': target['location']={'pdf_page':37,'column':'right','scope':'boundary_context','content_review':'visual occurrence observed, semantic target not verified'};status='external_location_observed_in_boundary_context'
        candidate(i['id'],target,'numeric','unknown',ref,i['evidence'],status)

NAMED=[('C-9.12-02','Missile Range and Results Chart','MRRC / Elephant Screen row','table_use'),('C-9.13-01','Missile Range and Results Chart','Mounted Javelinists','table_use'),('C-9.19-01','Clash of Spears and Swords Chart','Clash of','table_use'),('C-9.19-01','Shock Superiority Chart','Shock Superiority','table_use'),('X-02','Shock Combat Results Table','Shock Results Table','mention'),('X-04','Shock Combat Results Table','Shock CRT','mention'),('C-9.41-01','Shock Combat Results Table','Shock Combat CRT','table_use'),('C-9.61-01','Stacking Charts','Stacking Charts','table_use'),('N-14','Combat Tables (aggregate; exact chart(s) unknown)','Combat Tables','modification'),('C-9.96-03','Movement Cost Chart','Movement Cost Chart','table_use'),('C-9.96-07','Missile Range and Results Chart','MRRC / Mounted Javelin row','table_use'),('C-9.14-01','local rampage table','one of the following','table_use'),('TR-02','battle-specific map compass','Compass on the map','procedure_use'),('X-01','battle-specific map compass','compass on the map','procedure_use'),('C-9.66-01','local MLE diagram','see the diagram','mention')]
for f,t,q,k in NAMED:
    status='external_unresolved'; target={'name':t,'identifier':'unknown','alias_resolution':'provisional'}
    if t=='local rampage table': target['inventory_id']='T-01';status='internal_item_observed'
    if t=='local MLE diagram': target['inventory_id']='D-02';status='internal_item_observed'
    candidate(f,target,'named',k,q,by_id[f]['evidence'],status)

UNNUMBERED=[('C-9.11-01','front/rear hexes, ZOC and SHOCK MUST CHECK TQ marker','Front hexes','definition'),('C-9.11-08','general Shock resolution procedure','Shock resolution procedure','procedure_use'),('C-9.12-03','missile supply and supply markers','missile supply markers','procedure_use'),('C-9.13-01','Reaction Fire procedure','Reaction Fire','procedure_use'),('C-9.15-01','ZOC/facing and Attack Superiority','Attack Superiority','exception'),('C-9.16-01','Orderly Withdrawal, TQ check and routed state','Orderly Withdrawal','procedure_use'),('C-9.17-01','Position/Attack Superiority','Position Superiority','exception'),('C-9.18-01','leader command eligibility and exceptions','any leader','condition'),('C-9.21-01','Orderly Withdrawal base procedure','Orderly','modification'),('C-9.22-01','Missile Fire and H&D procedures','H&D','exception'),('C-9.23-03','Pre-Shock TQ check and marker','Pre-Shock TQ','exception'),('C-9.23-06','general Pre-Shock checks by unit types','Pre-Shock TQ','exception'),('C-9.24-02','rout procedure','Rout','exception'),('N-09','scenario-specific DD eligibility','scenario-specific rules','condition'),('C-9.51-01','Individual Order, Line Command, OC and terrain costs','Individual Order','procedure_use'),('C-9.53-03','TQ checks and rear-facing rules','TQ checks','modification'),('C-9.53-06','base flank/rear hit multiplier','instead of doubled','modification'),('C-9.53-08','rout and retreat procedure','rout','modification'),('X-06','Cynoscephalae scenario rules','scenario rules','mention'),('C-9.61-01','Roman/Velites stacking exceptions and LC eligibility','exceptions','condition'),('C-9.64-01','Individual Order and Line Command','Individual Order','exception'),('C-9.65-01','general facing movement cost','unlike most other units','modification'),('C-9.66-01','Orderly Withdrawal, Clear terrain, ZOC','Orderly Withdrawal','exception'),('C-9.67-01','Orderly Withdrawal trigger/sequence','Orderly Withdrawal','condition'),('C-9.68-01','Line Command and Column restrictions','Line Command','condition'),('C-9.7-01','scenario date and Overall Commander identity','200 BCE','condition'),('C-9.71-02','LOS and Triarii line definition','LOS','definition'),('C-9.71-03','Roman/Ala/allied line identity','Ala','definition'),('C-9.72-01','army Rout Points and Army Withdrawal Level','Army Withdrawal Level','condition'),('C-9.81-01','Light Infantry defense/movement and bolt fire','Light Infantry','definition'),('C-9.82-01','Individual Order and Orders Phase','Individual Order','procedure_use'),('C-9.83-01','general stacking restrictions','All other stacking rules','condition'),('C-9.85-01','Game Turn, Orders Phase, Movement and Missile Fire Segment','Game Turn','definition'),('C-9.86-01','enemy Orders Phase and Movement/Missile Segment','enemy Orders','definition'),('C-9.87-01','Cohesion Hit recovery and rout','as any other unit','procedure_use'),('C-9.93-02','Recovery order','Recovery order','modification'),('C-9.93-03','depletion and rout','Depleted','exception'),('C-9.94-02','Pre-Shock TQ procedure','Pre-Shock TQ','modification'),('C-9.94-03','scenario commander mapping and Initiative Rating','scenario','condition'),('C-9.95-02','Momentum procedure and scenario command mapping','Momentum','modification'),('C-9.96-02','eligible LI identity and Orderly Withdrawal','eligible Light Infantry','condition'),('C-9.96-03','general stacking restrictions and movement accounting','All other stacking restrictions','modification'),('C-9.96-05','repeat movement cohesion procedure','second (and','exception'),('C-9.96-06','LI Shock defense and dismount','defend as LI','condition'),('C-9.96-07','Harassment and Dispersal procedure','Harassment','procedure_use')]
for f,t,q,k in UNNUMBERED:
    candidate(f,{'name':t,'identifier':'unknown','target_source':'unknown'},'unnumbered',k,q,by_id[f]['evidence'],'unresolved','The quoted span names a procedure/definition or changes a general rule without a number. Necessity and exact target remain unverified; lexical similarity alone does not prove an executable dependency.')
for id,f,t,a,b,desc in CONT:
    candidate(id,{'inventory_id':t,'fragment':evidence(b)},'continuation','continuation',desc,evidence(a+';'+b),'internal_fragment_observed','Physical reading order: starting fragment → subsequent fragment; do not treat same parent item ID as a semantic self-dependency.')

history=json.loads((ROOT/'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json').read_text(encoding='utf-8'))
external=sorted({x['target_candidate']['identifier'] for x in candidates if x['category']=='numeric' and x['target_status'].startswith('external')})
assert set(external)==set(history['external_numeric_reference_candidates']),external
save(P/'evaluation/draft/dependency-candidates.json',{'artifact':'M-POC1A-dependency-candidates','version':'draft-v1','assessment_version':'draft_unfrozen','source_id':SOURCE_ID,'source_sha256':sha(SRC),'status':'candidates_only_waiting_review','direction_convention':'from = source unit that uses/mentions/modifies target; to remains null until review resolves target; continuation is fragment-start → fragment-end','historical_comparison':{'historical_manifest_sha256':sha(ROOT/'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json'),'historical_distinct_external_numeric_candidates':19,'observed_distinct_external_numeric_tokens':external,'matched':True,'added':[],'not_observed':[],'graph_verified':False},'counts':dict(Counter(x['category'] for x in candidates)),'candidates':candidates,'review':{'human_review':'pending','reviewer':None,'approved_graph':False},'limits':'No recursive closure, no external target pages beyond existing boundary context, no criticality assignment or situations.'})

evidence_files=[{'path':p.relative_to(P).as_posix(),'sha256':sha(p),'bytes':p.stat().st_size} for p in sorted(E.iterdir()) if p.is_file() and p.name!='author_inventory.py']
save(P/'source/source-v1.json',{'id':SOURCE_ID,'version':'source-v1','card':'M-POC1A','source':{'path':str(SRC),'exists':True,'bytes':SRC.stat().st_size,'sha256':sha(SRC),'page_count':44,'pdf_version':'1.7','page_size_points':[612,792],'publisher':'GMT Games, LLC','title':'SPQR: Great Battles of the Roman Republic','edition':'5th Edition','edition_evidence':{'pdf_page':1,'render':'source/review-evidence/edition-01.png','sha256':sha(E/'edition-01.png'),'observed_text':'RULE BOOK / 5th Edition'},'copyright_year_visible_in_core_headers':2026},'historical_input_comparison':{'path':'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json','manifest_sha256':sha(ROOT/'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/scope-candidates-v2.json'),'recorded_source_sha256':history['source_sha256'],'full_hash_match':True,'discrepancy':None,'proposal_path':'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/poc-plan-proposal.txt','proposal_sha256':sha(ROOT/'private/source-artifacts/SRC-spqr.rules/poc-scope-20261007/poc-plan-proposal.txt')},'scope':{'chapter':'9.0 SPECIAL COMBAT UNITS','pdf_pages_inclusive':[31,37],'numbering':'one-based PDF physical pages; printed labels31–37 agree','start':{'pdf_page':31,'column':'right','heading':'9.0','core_bbox':[315,309.4529,567,744],'glyph_top_pdfplumber':311.4529},'end':{'pdf_page':37,'column':'left','before_heading':'10.0','core_bbox':[45,45,297,392.6396],'heading_glyph_top_pdfplumber':393.6396},'boundary_coordinate_note':'Historical scope coordinates are valid whitespace cuts around headings; glyph envelopes differ by1–2 points due to text metrics. No source/hash or scope discrepancy.','column_order':'31 right core →32 left →32 right →33 left →33 right →34 left →34 right →35 left →35 right →36 left →36 right →37 left core','excluded_context':inventory['excluded_context'],'boundary_verification':'visually_checked_by_codex','owner_review':'pending'},'provenance':{'application':'Codex desktop','actual_model_visible_name':'unknown','reasoning_level':'unknown','available_system_description':'Codex based on GPT-6; UI model selector not inspected','read_is_inventory_session':True,'M_POC2B_run':False,'not_a_blind_extraction_session':True,'source_verification_time_utc':'2026-10-07T09:18:55Z','author':'Codex','human_reviewer':None},'tools':{'renderer':'pdftoppm26.07.0','render_dpi_core':150,'render_dpi_cover':100,'helper':'pdfplumber0.11.10','text_policy':'Auxiliary locator/transcription only; renders and logical column order determine observations'},'git_baseline':{'branch':'master','head':'0bd88a739f22f8bb8a1bebb0101a177bd05552c1','index_sha256':'6197ec7c5718aed38ecde9e66dd35a51a7dcd8ab715409faf7237c1c3d21c211','existing_changes':'M-POC0 reorganization; preserved','status_evidence':'source/review-evidence/git-status-before.txt','warning':'User-global ignore file inaccessible; per-command safe.directory used, no global configuration changed'},'evidence_files':evidence_files,'status':'source_verified_by_codex_waiting_owner_boundary_review'})
print(json.dumps({'inventory_counts':inventory['counts'],'candidate_counts':dict(Counter(x['category'] for x in candidates)),'candidate_total':len(candidates),'external_numeric_distinct':len(external)},indent=2))
