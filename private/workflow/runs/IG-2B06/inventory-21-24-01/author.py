"""Task-local independently authored page inventory; no historical derivation inputs."""
import copy
import json
from pathlib import Path
from wgc.sources.inventory import make_region, seal, validate, file_pin

ROOT = Path.cwd()
RUN = Path('private/workflow/runs/IG-2B06/inventory-21-24-01')
SESSION = Path('private/workflow/orchestrator/20261016T164231Z-37ee310d/002-IG-2B06-executor-cb5bccac')
load = lambda p: json.loads(Path(p).read_text(encoding='utf-8'))
meta = {k: load(RUN/'claim.json')[k] for k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256','task')}

def write(path, data):
    path=Path(path); path.parent.mkdir(parents=True,exist_ok=True)
    with path.open('x',encoding='utf-8',newline='\n') as f: json.dump(data,f,ensure_ascii=False,indent=2);f.write('\n')

def report(name, **data):
    write(RUN/name, dict(meta,**data))

# Boxes below were authored against fresh 1224 x 1584 original-page PNGs.
# A conservative outward conversion retains edge glyphs and rules.
def box(p):
    x0,y0,x1,y1=p
    return [x0*1000000//1224,y0*1000000//1584,(x1*1000000+1223)//1224,(y1*1000000+1583)//1584]

spec=[]
def add(p,key,kind,rect,description,components=None,uncertainty=None):
    spec.append(dict(page=p,key=key,kind=kind,box=box(rect),description=description,
                     components=components or [dict(name=description,box=box(rect))],
                     uncertainty=uncertainty or []))
def rows(p, entries):
    for key,kind,rect,desc in entries: add(p,key,kind,rect,desc)

for p in (21,22,23,24):
    add(p,'running-header','editorial',[88,44,1136,83],'Running title, edition, printed page number and horizontal rule',[
        dict(name='Running title and edition',box=box([414,50,811,73])),
        dict(name=f'Printed page label {p}',box=box([1110,45,1135,69] if p%2 else [88,45,114,69])),
        dict(name='Horizontal header rule',box=box([89,78,1135,82]))])

rows(21,[
('7.24-bullet-1','clause',[89,104,595,127],'Incoming 7.24 first condition bullet, continuing page 20 lead-in'),
('7.24-bullet-2','clause',[89,131,595,153],'Incoming 7.24 second condition bullet'),
('7.24-bullet-3','clause',[89,157,595,203],'Incoming 7.24 third condition bullet; wraps to second line'),
('7.24-exception','clause',[89,217,595,263],'7.24 exception paragraph'),
('7.24-design-note','note',[89,272,595,376],'Blue design note on facing changes; entire shaded box'),
('7.25','clause',[89,388,595,434],'7.25 shared ZOC paragraph'),
('7.3-heading','heading',[89,453,595,480],'7.3 Shock Requirements heading'),
('7.3-introduction','clause',[89,485,595,553],'7.3 introduction'),
('7.31','clause',[89,567,595,804],'7.31 complete paragraph including heavy/light alternatives'),
('7.32-marker','diagram',[89,825,164,901],'Shock Must Check TQ marker: border, red/black words, white field'),
('7.32-opening','clause',[178,818,595,913],'7.32 opening text to right of marker; ends with line-broken mark-'),
('7.32-completion','clause',[89,915,595,984],'7.32 remainder below marker, beginning ers are placed'),
('7.32-example','example',[89,997,595,1161],'Complete italic Macedonian Phalanx and Numidian cavalry example'),
('7.33-marker','diagram',[89,1183,164,1259],'Shock No TQ Check marker: border and complete word stack'),
('7.33-opening','clause',[178,1175,595,1271],'7.33 text beside marker through friendly ZOCs'),
('7.33-completion','clause',[89,1272,595,1365],'7.33 continuation below marker and introduction-to-8.4 reference'),
('7.33-exceptions-label','heading',[89,1378,595,1403],'Exceptions label'),
('7.33-exception-1','clause',[89,1409,595,1456],'First exception bullet: named unit classes'),
('7.33-exception-2','clause',[629,104,1135,127],'Second exception bullet at top of right column'),
('7.33-exception-3','clause',[629,131,1135,154],'Third exception bullet, Velites'),
('7.33-engaged','clause',[629,167,1135,236],'Engaged rule paragraph'),
('7.33-play-note','note',[629,245,1135,350],'Complete gray play note'),
('8.0-heading','heading',[629,382,1135,418],'8.0 Combat blue section heading'),
('8.0-introduction','clause',[629,424,1135,638],'Complete combat introduction'),
('8.1-heading','heading',[629,656,1135,683],'8.1 Missile Fire heading'),
('8.1-history','note',[629,684,1135,887],'Complete tan historical note'),
('8.11-sample-j','diagram',[629,910,704,986],'Thrace javelin sample counter, J and complete counter face'),
('8.11-sample-a','diagram',[706,910,781,986],'Crete archer sample counter, A and complete counter face'),
('8.11-sample-s','diagram',[783,910,858,986],'Balearic slinger sample counter, S and complete counter face'),
('8.11-sample-scorpio','diagram',[861,910,936,986],'Scorpio sample counter and complete counter face'),
('8.11-opening','clause',[950,902,1135,995],'8.11 text to right of four sample counters'),
('8.11-completion','clause',[629,997,1135,1164],'8.11 continuation below counters through once per Orders Phase'),
('8.11-exception','clause',[629,1178,1135,1248],'8.11 exception paragraph'),
('8.11-history','note',[629,1257,1135,1316],'Tan historical note on pilum/javelin naming'),
('8.11-examples','example',[629,1331,1135,1426],'Complete mounted archer and slinger movement examples'),
])
rows(22,[
('8.12','clause',[89,104,595,196],'8.12 complete paragraph'),
('8.13','clause',[89,211,595,376],'8.13 complete paragraph above missile arc diagram'),
('8.14','clause',[89,726,595,988],'8.14 complete LOS paragraph below diagram'),
('8.14-exceptions-label','heading',[89,1001,595,1025],'Exceptions label'),
('8.14-exception-1','clause',[89,1031,595,1099],'Archer LOS exception bullet'),
('8.14-exception-2','clause',[89,1105,595,1150],'Line Commands/Elephant LOS exception bullet'),
('8.14-play-note','note',[89,1161,595,1242],'Gray LOS play note'),
('8.15-opening','clause',[89,1253,595,1442],'8.15 missile fire resolution paragraph through otherwise on'),
('8.15-completion','clause',[629,104,1135,149],'8.15 across-column continuation beginning the chart'),
('8.15-drms','clause',[629,163,1135,233],'DRM exception paragraph'),
('8.15-design-note','note',[629,243,1135,515],'Blue foot-javelinists design note'),
('8.15-example','example',[629,527,1135,741],'Complete Cannae slingers example'),
('8.16','clause',[629,752,1135,822],'8.16 Extended Range paragraph'),
('8.17-introduction','clause',[629,836,1135,881],'8.17 Missile Supply introduction opening two lines'),
('8.17-availability','clause',[629,884,1048,905],'8.17 introduction last line, availability level, beside marker'),
('8.17-bullet-1','clause',[629,914,1047,1035],'First supply bullet, narrower beside markers'),
('8.17-marker-no','diagram',[1061,901,1136,977],'Missile No marker, complete face and border'),
('8.17-marker-low','diagram',[1061,980,1136,1056],'Missile Low marker, complete face and border'),
('8.17-bullet-2-opening','clause',[629,1040,1048,1063],'Second supply bullet opening beside lower marker'),
('8.17-bullet-2-completion','clause',[629,1064,1135,1134],'Second supply bullet completion below markers'),
('8.17-bullet-3','clause',[629,1138,1135,1207],'Third supply bullet, Legion Infantry'),
('8.17-bullet-4','clause',[629,1213,1135,1283],'Fourth supply bullet, javelin-armed infantry'),
('8.17-bullet-5','clause',[629,1288,1135,1335],'Fifth supply bullet, flipping marker'),
])

# An indivisible compound diagram retains overprinted labels/counters/arrows and
# shared hex edges. Components are explicitly itemized within the one crop;
# overlapping component bounds never become overlapping denominator regions.
add(22,'8.13-missile-arc','diagram',[89,400,596,723],
    'Complete missile arc diagram; compound because arrows and labels overlay the connected hex field',[
        dict(name='Connected five-column hex field: all outlines and green/gray/yellow fills',box=box([89,400,596,723])),
        dict(name='Central Iberia skirmisher counter: whole face, J, values and border',box=box([313,565,375,629])),
        *[dict(name=n,box=box(b)) for n,b in [
            ('Left Front label',[154,443,195,463]),('Right Front label',[493,443,535,463]),
            ('Left Flank label',[113,662,157,682]),('Right Flank label',[533,662,578,682]),
            ('Green dashed north-west arrow',[257,448,341,593]),('Green dashed north arrow',[339,448,347,568]),
            ('Green dashed north-east arrow',[348,448,430,594]),('Green dashed west-north-west arrow',[217,522,317,585]),
            ('Green dashed east-north-east arrow',[372,522,471,585]),('Green dashed west arrow',[173,590,315,604]),
            ('Green dashed east arrow',[373,590,512,604]),('Green dashed south-west arrow',[216,607,319,674]),
            ('Green dashed south-east arrow',[371,607,472,674])]]] )

rows(23,[
('8.17-design-note','note',[89,107,595,644],'Entire blue design note on pila and artistic depiction'),
('8.17-play-note-introduction','note',[89,657,595,756],'Gray play note introduction on single-shot LG units'),
('8.17-play-note-item-1','note',[89,766,595,791],'Gray play note numbered condition 1'),
('8.17-play-note-item-2','note',[89,799,595,940],'Gray play note numbered condition 2 and marker timing paragraph'),
('8.17-play-note-completion','note',[89,952,595,1051],'Gray play note final paragraph'),
('8.18-introduction','clause',[89,1063,595,1157],'8.18 Reload introduction'),
('8.18-bullet-1','clause',[89,1165,595,1188],'8.18 first condition bullet'),
('8.18-bullet-2','clause',[89,1191,595,1237],'8.18 second condition bullet'),
('8.19','clause',[89,1250,595,1416],'8.19 Leader Casualties complete paragraph'),
('8.2-heading','heading',[629,103,1135,130],'8.2 Reaction Fire heading'),
('8.2-introduction','clause',[629,136,1135,253],'8.2 introduction'),
('8.21','clause',[629,266,1135,409],'8.21 Entry Reaction paragraph'),
('8.21-exception','clause',[629,420,1135,514],'8.21 exception paragraph'),
('8.22','clause',[629,528,1135,645],'8.22 Retire Reaction paragraph'),
('8.22-exception','clause',[629,659,1135,705],'8.22 exception paragraph'),
('8.23','clause',[629,717,1135,835],'8.23 Return Fire paragraph'),
('8.24','clause',[629,848,1135,942],'8.24 paragraph'),
('8.25','clause',[629,954,1135,1000],'8.25 paragraph'),
('8.3-heading','heading',[629,1019,1135,1046],'8.3 Harassment & Dispersal heading'),
('8.3-history','note',[629,1047,1135,1105],'Tan historical note'),
('8.31','clause',[629,1121,1135,1287],'8.31 complete paragraph'),
('8.31-exceptions-label','heading',[629,1300,1135,1325],'Exceptions label'),
('8.31-exception-1','clause',[629,1331,1135,1376],'First H&D exception bullet'),
('8.31-exception-2','clause',[629,1382,1135,1428],'Second H&D exception bullet'),
])
rows(24,[
('8.32','clause',[89,104,595,318],'8.32 complete H&D eligibility/path paragraph'),
('8.33-introduction','clause',[89,331,595,377],'8.33 procedure introduction'),
('8.33-bullet-1','clause',[89,385,595,408],'8.33 first procedure bullet'),
('8.33-bullet-2','clause',[89,412,595,435],'8.33 second procedure bullet'),
('8.33-bullet-3','clause',[89,439,595,485],'8.33 third procedure bullet and moving-attack sentence'),
('8.33-reaction','clause',[89,497,595,615],'8.33 reaction paragraph'),
('8.33-no-physical-move','clause',[89,627,595,674],'8.33 physical movement clarification paragraph'),
('8.33-design-note','note',[89,684,595,812],'Blue H&D movement design note'),
('8.34','clause',[89,823,595,940],'8.34 complete elephants paragraph'),
('8.34-example-opening','example',[89,1414,595,1460],'Beneventum example opening below diagram, continuing top right'),
('8.34-example-a','example',[629,104,1135,197],'Example A continuation at top right'),
('8.34-example-b','example',[629,211,1135,305],'Example B paragraph'),
('8.34-example-c','example',[629,318,1135,533],'Example C paragraph'),
('8.34-example-d','example',[629,546,1135,832],'Example D paragraph'),
('8.4-heading','heading',[629,849,1135,877],'8.4 Shock Combat heading'),
('8.4-design-note','note',[629,878,1135,1030],'Blue shock design note'),
('8.4-play-note','note',[629,1043,1135,1195],'Gray shock play note'),
('8.4-procedure-heading','heading',[629,1211,1135,1235],'Procedure heading'),
('8.4-procedure','clause',[629,1239,1135,1333],'Shock procedure paragraph'),
('8.4-important','note',[629,1345,1136,1456],'Complete red Important box including border and sequence paragraph'),
])
add(24,'8.34-beneventum-diagram','diagram',[98,955,590,1406],
    'Complete Beneventum compound hex diagram; overprinted counters, labels and crossing arrows require a single non-overlapping denominator region',[
        dict(name='Connected hex field: all white cells and shared gray outlines',box=box([98,955,590,1406])),
        *[dict(name=n,box=box(b)) for n,b in [
            ('A Crete archer counter, whole face and border',[197,1053,261,1121]),('A label',[145,1041,167,1067]),
            ('B Thrace peltast counter, whole face and border',[340,1053,405,1121]),('B label',[330,1031,352,1056]),
            ('C Thrace peltast counter, whole face and border',[272,1108,337,1175]),('C label',[248,1160,272,1186]),
            ('D Macedon light cavalry counter, whole face and border',[197,1238,261,1305]),('D label',[216,1310,239,1337]),
            ('W Roman counter, whole face and border',[426,1010,491,1078]),('W label',[499,1006,526,1035]),
            ('X Roman counter, whole face and border',[426,1100,491,1166]),('X label',[500,1095,525,1126]),
            ('Y Roman counter, whole face and border',[426,1188,491,1255]),('Y label',[500,1186,525,1215]),
            ('Z Roman counter, whole face and border',[426,1277,491,1345]),('Z label',[500,1275,525,1305]),
            ('A dashed gray arrow to Y',[250,1096,428,1216]),('A dashed gray arrow to Z',[228,1115,428,1299]),
            ('B black arrow to W',[399,1051,430,1086]),('B black arrow to X',[400,1099,430,1123]),
            ('C black H&D arrow to Y',[333,1164,429,1219]),
            ('D orange arrow to X',[258,1156,418,1268]),('D orange arrow to Y',[258,1220,419,1274]),
            ('D orange arrow to Z',[258,1274,418,1317])]]] )

for p in (21,22,23,24):
    add(p,'copyright-footer','editorial',[524,1497,700,1518],'Copyright 2026 GMT Games LLC footer')

def main():
    contract=load('private/workflow/runs/IG-2B06/refinement-1bcd2b72-01/refinement-contract.json')
    baseline=load(contract['input_pins'][0]['path']); reg=load(contract['input_pins'][1]['path'])
    assert baseline['registry']==reg
    validate(baseline,ROOT)
    doc=copy.deepcopy(baseline)
    targets={x['id'] for x in contract['placeholder_targets']}
    assert {r['id'] for r in baseline['regions'] if r['page_id'] in {p['id'] for p in baseline['pages'] if p['pdf_page'] in (21,22,23,24)}}==targets
    doc['regions']=[r for r in doc['regions'] if r['id'] not in targets]
    added=[]
    for s in spec:
        page=next(p for p in doc['pages'] if p['pdf_page']==s['page'])
        r=make_region(reg,'ig2b06:'+str(s['page'])+':'+s['key'],page,s['box'],kind=s['kind'],reason='Source region inventoried; verified transcription and semantic representation remain pending.')
        r['uncertainty']=s['uncertainty']
        r['coverage']['transcription']={'status':'partial','gap':True,'reason':'Fresh machine text/image evidence is required; no verified complete transcription or human decision.','boundary':None}
        r=seal(r); added.append(r);s['region_id']=r['id']
    # Only the exact coordinator-authorized narrow regions on pages 20 and 25.
    for p,b,key,desc in [(20,[500000,730000,940000,930000],'incoming-context','Authorized lower-right page-20 crop including 7.24 lead-in'),(25,[60000,60000,940000,410000],'outgoing-context','Authorized upper page-25 sequence context; bottom text is clipped at the contract boundary')]:
        page=next(p0 for p0 in doc['pages'] if p0['pdf_page']==p)
        r=make_region(reg,'ig2b06:'+key,page,b,kind='clause',role='context',reason='Context only; page outside assigned inventory scope.')
        added.append(r);spec.append(dict(page=p,key=key,kind=r['kind'],box=b,region_id=r['id'],description=desc,components=[dict(name=desc,box=b)],uncertainty=['Crop boundary intentionally limits surrounding context.']))
    doc['regions']+=added;doc['registry']=reg
    bykey={s['key']:s['region_id'] for s in spec}
    # Reading order is explicitly authored, including wraps and the two columns.
    orders={21:['running-header','7.24-bullet-1','7.24-bullet-2','7.24-bullet-3','7.24-exception','7.24-design-note','7.25','7.3-heading','7.3-introduction','7.31','7.32-marker','7.32-opening','7.32-completion','7.32-example','7.33-marker','7.33-opening','7.33-completion','7.33-exceptions-label','7.33-exception-1','7.33-exception-2','7.33-exception-3','7.33-engaged','7.33-play-note','8.0-heading','8.0-introduction','8.1-heading','8.1-history','8.11-sample-j','8.11-sample-a','8.11-sample-s','8.11-sample-scorpio','8.11-opening','8.11-completion','8.11-exception','8.11-history','8.11-examples','copyright-footer'],
            22:['running-header','8.12','8.13','8.13-missile-arc','8.14','8.14-exceptions-label','8.14-exception-1','8.14-exception-2','8.14-play-note','8.15-opening','8.15-completion','8.15-drms','8.15-design-note','8.15-example','8.16','8.17-introduction','8.17-availability','8.17-bullet-1','8.17-marker-no','8.17-marker-low','8.17-bullet-2-opening','8.17-bullet-2-completion','8.17-bullet-3','8.17-bullet-4','8.17-bullet-5','copyright-footer'],
            23:[s['key'] for s in spec if s['page']==23],
            24:['running-header','8.32','8.33-introduction','8.33-bullet-1','8.33-bullet-2','8.33-bullet-3','8.33-reaction','8.33-no-physical-move','8.33-design-note','8.34','8.34-beneventum-diagram','8.34-example-opening','8.34-example-a','8.34-example-b','8.34-example-c','8.34-example-d','8.4-heading','8.4-design-note','8.4-play-note','8.4-procedure-heading','8.4-procedure','8.4-important','copyright-footer']}
    lookup={(s['page'],s['key']):s['region_id'] for s in spec}
    old_byid={r['id']:r for r in baseline['regions']};old_pages={p['id']:p['pdf_page'] for p in baseline['pages']}
    doc['reading_order']=[]
    for rid in baseline['reading_order']:
        if rid in targets: doc['reading_order'] += [lookup[(old_pages[old_byid[rid]['page_id']],k)] for k in orders[old_pages[old_byid[rid]['page_id']]]]
        else: doc['reading_order'].append(rid)
    # Context appended explicitly: existing nonassigned relative order is untouched.
    doc['reading_order'] += [bykey['incoming-context'],bykey['outgoing-context']]
    newlinks=[]
    def link(a,b,reason,kind='continuation'):
        newlinks.append(dict(kind=kind,**{'from':bykey[a],'to':bykey[b]},reason=reason))
    for a,b,reason in [
        ('incoming-context','7.24-bullet-1','7.24 lead-in on page 20 continues with three conditions on page 21.'),
        ('7.24-bullet-1','7.24-bullet-2','Consecutive 7.24 condition bullets.'),('7.24-bullet-2','7.24-bullet-3','Consecutive 7.24 condition bullets.'),
        ('7.32-opening','7.32-completion','Text wraps below marker; mark-/ers split is preserved.'),
        ('7.33-opening','7.33-completion','Paragraph wraps below marker.'),
        ('7.33-exception-1','7.33-exception-2','Exceptions continue from left column bottom to right column top.'),
        ('7.33-exception-2','7.33-exception-3','Third exception bullet.'),
        ('8.11-opening','8.11-completion','Text wraps below four sample counters.'),
        ('8.11-examples','8.12','8.1 sequence boundary across pages 21/22; preceding example is complete.'),
        ('8.15-opening','8.15-completion','8.15 sentence continues from left bottom to right top.'),
        ('8.17-introduction','8.17-availability','Introduction wraps beside the top of the Missile No marker.'),
        ('8.17-bullet-2-opening','8.17-bullet-2-completion','Supply bullet wraps below marker; Mis-/sile split retained.'),
        ('8.17-bullet-5','8.17-design-note','8.17 notes continue on page 23; bullet text on page 22 is complete.'),
        ('8.17-play-note-introduction','8.17-play-note-item-1','Numbered condition within same gray play note.'),
        ('8.17-play-note-item-1','8.17-play-note-item-2','Second numbered condition and marker timing.'),
        ('8.17-play-note-item-2','8.17-play-note-completion','Final paragraph of same note.'),
        ('8.31-exception-2','8.32','8.3 rule sequence continues on page 24; exception text is complete.'),
        ('8.34-example-opening','8.34-example-a','Example continues from page-24 left-column bottom to right-column top.'),
        ('8.34-example-a','8.34-example-b','Consecutive lettered example discussion.'),('8.34-example-b','8.34-example-c','Consecutive lettered example discussion.'),('8.34-example-c','8.34-example-d','Consecutive lettered example discussion.'),
        ('8.4-important','outgoing-context','8.4 procedure/sequence continues on page 25; page-24 Important text is complete. Context only, no page-25 inventory.')]: link(a,b,reason)
    for a,b in [('7.32-marker','7.32-opening'),('7.33-marker','7.33-opening'),('8.13-missile-arc','8.13'),('8.34-beneventum-diagram','8.34-example-opening'),('8.17-marker-no','8.17-introduction'),('8.17-marker-low','8.17-introduction')]:link(a,b,'Image supports adjacent source text; no gameplay interpretation accepted.','illustrates')
    for a in ['8.11-sample-j','8.11-sample-a','8.11-sample-s','8.11-sample-scorpio']:link(a,'8.11-opening','Sample counter group illustrates missile capability classes.','illustrates')
    doc['links']+=newlinks
    doc=seal(doc);validate(doc,ROOT)
    write(RUN/'authored/inventory.json',doc);write(RUN/'authored/identity-registry.json',reg)
    report('authored-regions.json',summary='Independent source-authored regions and component map from fresh original renders.',regions=spec,new_links=newlinks,coordinate_basis='Integer normalized half-open page millionths; authored pixel boxes outward-rounded from 144-DPI 1224x1584 originals.',semantic_acceptance=False,executable_readiness=False)
    report('checkpoint-authored.json',summary='Authored complete assigned ledger and two context regions, preserving baseline internally.',artifacts=[file_pin(ROOT,(RUN/p).as_posix()) for p in ['authored/inventory.json','authored/identity-registry.json','authored-regions.json']],completed_criteria=['Fresh visual inspection of all assigned pages and two narrow context crops','Independent authored regions/components and explicit reading order'],next_operation='Generate two complete independent evidence replays and fresh final locators.',blocker=None)
    print(json.dumps({'assigned_regions':len([s for s in spec if s['page'] in (21,22,23,24)]),'context_regions':2,'new_links':len(newlinks)}))

if __name__=='__main__':main()
