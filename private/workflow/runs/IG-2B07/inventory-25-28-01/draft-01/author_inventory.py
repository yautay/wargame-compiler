"""Explicit executor-authored page accounting in original 144-DPI pixel coordinates.

Coordinates are converted to the canonical page-millionth frame. Components are
nested context observations, never additional inventory denominator memberships.
"""
import json
import hashlib
from pathlib import Path

A = Path(__file__).parent
rows = []
def add(page, key, kind, box, observation, role='inventory', category='body'):
    rows.append(dict(page=page,key='ig2b07:'+key,kind=kind,
                     box=[v*1000000//(1224 if i%2==0 else 1584) for i,v in enumerate(box)],
                     observation=observation,role=role,category=category))
def vertical(page, specs, x0=90, x1=594):
    for key,kind,y0,y1,text in specs:
        add(page,key,kind,[x0,y0,x1,y1],text)

for page in (25,26,27,28):
    add(page,f'p{page}-running-header','editorial',[90,45,1135,82],f'Running title, printed page {page}, and header rule; editorial accounting, no human exclusion claimed.',category='editorial')

vertical(25,[
 ('p25-play-note','note',107,212,'Grey play note on sequencing separate Shock steps; visibly follows page-24 procedure context.'),
 ('p25-design-note','note',225,448,'Blue design note on isolated Shock resolution; entire shaded panel.'),
 ('p25-841','clause',460,554,'8.41 Shock Designation, including marker choices and final attack sentence.'),
 ('p25-842-intro','clause',568,709,'8.42 basic procedure introduction through restrictions lead-in.'),
 ('p25-842-b1','clause',715,742,'First restriction bullet: once per combat segment.'),
 ('p25-842-b2','clause',742,792,'Second restriction bullet, including pursuit exception reference.'),
 ('p25-842-b3','clause',792,842,'Third restriction bullet, multiple defenders and front zones.'),
 ('p25-842-b4','clause',842,916,'Fourth restriction bullet, no split and combined attack qualification.'),
 ('p25-842-b5','clause',916,968,'Fifth restriction bullet on total Sizes.'),
 ('p25-842-b6','clause',968,999,'Sixth restriction bullet on stacked units.'),
 ('p25-842-tail','clause',1005,1055,'Closing paragraph allowing division subject to the restrictions.'),
 ('p25-example1','example',1065,1281,'Cannae example 1, complete italic paragraph.'),
 ('p25-example2','example',1290,1461,'Cannae example 2, complete italic paragraph.')])
vertical(25,[
 ('p25-resolution-title','heading',104,127,'Shock Resolution heading.'),
 ('p25-overview-subtitle','heading',130,156,'Italic overview subtitle.'),
 ('p25-overview-intro','clause',165,213,'Overview introduction naming sections 8.43 through 8.47.'),
 ('p25-overview1','clause',224,273,'Overview step 1, pre-Shock TQ.'),
 ('p25-overview2','clause',276,301,'Overview step 2, leader casualties.'),
 ('p25-overview3','clause',303,352,'Overview step 3, chart selection.'),
 ('p25-overview4','clause',355,404,'Overview step 4, modifiers.'),
 ('p25-overview5','clause',407,432,'Overview step 5, resolution.'),
 ('p25-overview6','clause',435,461,'Overview step 6, rout.'),
 ('p25-843-intro','clause',473,643,'8.43 Charge introductory paragraph and both marker cases.'),
 ('p25-843-exempt-intro','clause',652,678,'Exemption list lead-in.'),
 ('p25-843-exempt1','clause',681,705,'Exemption bullet for attacking a Skirmisher.'),
 ('p25-843-exempt2','clause',708,733,'Exemption bullet for attacking a routed unit.'),
 ('p25-843-exempt3','clause',735,786,'Exemption bullet for PH/HI/LG attacked frontally by LI.'),
 ('p25-843-dr','clause',792,841,'DR comparison and Cohesion Hits paragraph; continues on page 26.'),
 ('p25-843-defender','clause',846,941,'Defender rout bullet, exception reference and advance qualifications.'),
 ('p25-843-attacker','clause',944,1016,'Attacker rout bullet and no defender advance.'),
 ('p25-843-all','clause',1020,1092,'All attacking and defending units rout bullet and procedure reference.'),
 ('p25-rider-art','diagram',1106,1458,'Decorative mounted warrior artwork; recorded without a semantic exclusion.')],630,1134)

vertical(26,[
 ('p26-dr-mod-intro','clause',104,130,'DR modifier list lead-in continuing 8.43 from page 25.'),
 ('p26-mod1','clause',134,183,'Modifier row +1 Elephant frontal PH/HI.'),
 ('p26-mod2','clause',186,236,'Modifier row +1 African and Indian Elephant.'),
 ('p26-mod3','clause',238,264,'Modifier row +1 attacked by Double Depth Phalanx.'),
 ('p26-mod4','clause',267,293,'Modifier row minus 1 Double Depth Phalanx attacked.'),
 ('p26-mod5','clause',295,319,'Modifier row minus 1 BI Ferocity.'),
 ('p26-mod6','clause',322,372,'Modifier row +2 attacked by BI Ferocity.'),
 ('p26-phalanx-exception','clause',382,525,'Two-hex Phalanx exception, complete paragraph.'),
 ('p26-pre-shock-close','clause',538,586,'Closing paragraph for all pre-Shock TQ checks.'),
 ('p26-844','clause',597,717,'8.44 Shock and Leaders, complete paragraph.'),
 ('p26-845','clause',728,992,'8.45 Clash of Spears and Swords, chart and multiple-unit selection paragraph.'),
 ('p26-845-tail','clause',1002,1050,'Paragraph on non-Shock-capable units defending in conjunction.'),
 ('p26-example1','example',1061,1110,'8.45 example 1, complete paragraph.'),
 ('p26-example2','example',1120,1409,'8.45 example 2, complete paragraph.')])
vertical(26,[
 ('p26-example3','example',104,225,'8.45 example 3, top of right column.'),
 ('p26-846','clause',237,308,'8.46 Hand-to-Hand Struggle introduction.'),
 ('p26-step1','clause',320,489,'Step 1 Determine Superiority introduction.'),
 ('p26-position','clause',499,619,'A Position Superiority introduction.'),
 ('p26-position-list','clause',628,654,'Position Superiority exclusions lead-in.'),
 ('p26-position-b1','clause',657,682,'Skirmisher flank exception bullet.'),
 ('p26-position-b2','clause',684,709,'Cavalry attacks Elephant exception bullet.'),
 ('p26-position-b3','clause',711,736,'Elephant attacks Elephant exception bullet.'),
 ('p26-position-b4','clause',738,788,'Attacking unit enemy ZOC exception bullet.'),
 ('p26-position-tail','clause',797,894,'Paragraph relating above situations to Weapon System and Attack Superiority.'),
 ('p26-weapon','clause',904,1048,'B Weapon System Superiority, complete paragraph.'),
 ('p26-play-note','note',1055,1209,'Grey play note, including humorous closing phrase.'),
 ('p26-step2','clause',1220,1387,'Step 2 Determine Size Ratio Difference introduction through rounding lead-in.'),
 ('p26-step2-b1','clause',1392,1463,'First rounding bullet; list continues at page-27 left top.')],630,1134)

vertical(27,[
 ('p27-step2-b2','clause',104,176,'Second rounding bullet, continuation of page-26 Step 2.'),
 ('p27-srd-intro','clause',188,214,'SRD ignored situations lead-in.'),
 ('p27-srd-b1','clause',216,266,'Elephant versus non-Elephant bullet.'),
 ('p27-srd-b2','clause',268,293,'All defenders Skirmishers bullet.'),
 ('p27-ratio-example','example',303,398,'Italic size-ratio example, complete paragraph.'),
 ('p27-design-note','note',407,461,'Blue rounding/momentum design note.'),
 ('p27-step3','clause',475,690,'Step 3 Adjust Columns and Resolve, including leader-death modifier.'),
 ('p27-leader-example','example',700,820,'Italic Hannibal/Maharbal example.'),
 ('p27-step4','clause',833,904,'Step 4 Apply Results lead-in.'),
 ('p27-result-b1','clause',909,959,'Attack Superiority bullet.'),
 ('p27-result-b2','clause',960,1009,'Defense Superiority bullet.'),
 ('p27-result-b3','clause',1010,1060,'Skirmisher result bullet including maximum.'),
 ('p27-result-b4','clause',1061,1180,'Light Cavalry result bullet with exception and cumulative qualification.'),
 ('p27-result-tail','clause',1192,1241,'Final paragraph distributing Cohesion Hits.')])
vertical(27,[
 ('p27-847','clause',104,176,'8.47 Collapse introduction and explicit step order.'),
 ('p27-collapse1','clause',189,308,'Collapse step 1, including simultaneous rout and defender-first sentences.'),
 ('p27-collapse-ex1','clause',320,440,'Phalanx exception for step 1.'),
 ('p27-collapse2','clause',450,594,'Collapse step 2, including Phalanx procedure reference.'),
 ('p27-collapse-ex2','clause',604,653,'No second roll exception.'),
 ('p27-collapse3','clause',664,737,'Collapse step 3 and cavalry pursuit reference.'),
 ('p27-engaged','clause',747,939,'Optional Engaged rule paragraph, complete including both sides remaining.'),
 ('p27-play-note','note',945,1096,'Grey play note on order and tracking routed units.')],630,1134)

vertical(28,[
 ('p28-title','heading',104,132,'Extended Shock Example, Bagradas Plains.'),
 ('p28-designation','example',136,424,'Shock Designation example paragraph, including Bostar and four Carthaginian units.'),
 ('p28-procedure','example',435,625,'Pre-Shock Procedure example paragraph; all named target groups.'),
 ('p28-diagram-before','diagram',630,1272,'First full hex-grid diagram: pre-resolution positions, attacks, Shock and hit markers.'),
 ('p28-charge-start','example',1277,1468,'The Charge starts in left column; final sentence continues at right-column top.')])
vertical(28,[
 ('p28-charge-end','example',104,176,'The Charge sentence continuation: Triarii W routs; Phalanx B does not advance.'),
 ('p28-diagram-after','diagram',194,821,'Second full hex-grid diagram: W rout arrow and revised hit markers.'),
 ('p28-leaders','example',829,947,'Leader Casualties example paragraph, complete.'),
 ('p28-struggle-a','example',959,1343,'Hand-to-Hand Struggle example, full Phalanx A paragraph.'),
 ('p28-struggle-b','example',1353,1470,'Phalanx B example paragraph begins; final phrase continues on page 29.')],630,1134)

for page in (25,26,27,28):
    add(page,f'p{page}-copyright','editorial',[520,1495,705,1519],'Copyright footer; accounted as editorial, no authorized semantic exclusion.',category='editorial')

add(24,'entry-context','clause',[630,1218,1135,1454],'Page-24 bottom-strip Procedure and Important box; only boundary context, no denominator.',role='context',category='boundary')
add(29,'exit-context','example',[90,104,594,275],'Page-29 upper-left continuation of Phalanx B example, ending before next paragraph.',role='context',category='boundary')

def component(parent, name, box, text, page=28, kind='diagram'):
    add(page,parent+'-'+name,kind,box,text,role='context',category='component')
    rows[-1]['parent_key']='ig2b07:'+parent

# Decorative artwork is retained as source evidence, including its visible pieces.
for name,box,text in [
 ('lance',[746,1107,1039,1250],'Long diagonal lance, spearhead and shaft.'),
 ('rider',[815,1141,983,1395],'Helmeted mounted figure, clothing, limbs and purple cloak.'),
 ('shield',[792,1201,863,1329],'Blue shield and central boss.'),
 ('horse',[720,1194,1029,1456],'Horse, saddle, bridle, reins and harness.')]:
    component('p25-rider-art',name,box,text,page=25)

# Every named unit/counter, stack marker, attack arrow and diagram label is explicit.
# The hex grid is one repeated background component per diagram; no hidden cells are
# treated as rules, and all visible grid strokes remain in its pinned crop.
for parent,coords in [
 ('p28-diagram-before',dict(grid=[110,631,578,1270],bostar=[192,729,253,791],a=[274,693,337,816],b=[276,867,339,987],c=[272,1107,333,1171],d=[268,1190,328,1253],t=[348,648,410,709],u=[349,730,412,792],v=[350,809,412,872],w=[350,895,412,958],x=[350,982,412,1045],y=[350,1062,412,1125],z=[350,1146,413,1209],leader=[371,800,432,860],shocka=[254,680,317,741],shockb=[255,846,318,908],shockc=[232,1065,295,1126],hitw=[392,917,451,977],hitx=[393,998,451,1056],hitc=[235,1127,296,1187],hity=[393,1080,451,1139],hitz=[392,1164,452,1224],aa=[314,685,353,719],au=[325,741,353,768],av=[324,797,353,827],bw=[324,883,354,917],bx=[326,969,355,1001],cy=[325,1105,354,1138],cz=[325,1142,354,1171])),
 ('p28-diagram-after',dict(grid=[651,195,1117,820],bostar=[731,286,793,349],a=[815,252,878,370],b=[816,422,879,544],c=[813,660,874,723],d=[811,743,873,806],t=[890,200,952,263],u=[891,283,953,347],v=[891,366,954,429],w=[1033,449,1097,513],x=[891,535,954,598],y=[891,617,954,680],z=[891,699,954,763],leader=[911,354,975,417],shocka=[795,235,857,296],shockb=[796,398,859,461],shockc=[774,618,836,680],hitu=[935,293,993,354],hitv=[936,389,995,450],hitx=[936,549,994,610],hitc=[776,680,837,740],hity=[936,631,995,692],hitz=[936,714,995,777],rout=[1041,477,1103,535],routarrow=[948,466,1036,498],aa=[853,240,891,269],au=[866,299,895,327],av=[866,355,896,382],bx=[864,530,896,560],cy=[862,658,894,686],cz=[861,695,894,723]))]:
    labels = {'bostar':'Bostar leader counter','a':'Phalanx A double-size counter, printed values and symbols','b':'Phalanx B double-size counter, printed values and symbols','c':'Celt MI C counter','d':'Celt MI D counter','t':'Roman Velites T counter','u':'Roman cohort U counter','v':'Roman cohort V counter','w':'Roman Triarii W counter','x':'Roman Velites X counter','y':'Roman Triarii Y counter','z':'Roman Velites Z counter','leader':'Tribune Antonius leader counter stacked with V','shocka':'Shock Must Check TQ marker on A','shockb':'Shock Must Check TQ marker on B','shockc':'Shock No TQ Check marker on C','hitw':'3-hit marker by W','hitx':'1-hit marker by X','hitc':'2-hit marker under C','hitu':'1-hit marker by U','hitv':'2-hit marker by V','hity':'3-hit marker by Y','hitz':'4-hit marker by Z','rout':'Routed TQ-minus-1 marker on W','routarrow':'Yellow rightward rout arrow','aa':'Attack arrow A to T','au':'Attack arrow A to U','av':'Attack arrow A to V','bw':'Attack arrow B to W','bx':'Attack arrow B to X','cy':'Attack arrow C to Y','cz':'Attack arrow C to Z','grid':'Complete visible hex-grid background; grid/counter overlaps retained in nested observation.'}
    for name,box in coords.items():
        component(parent,name,box,labels[name])
    # Each external letter is a separate observed annotation.
    positions = [('a',249,803),('b',250,918),('c',209,1136),('d',245,1216),('t',421,661),('u',421,745),('v',430,826),('w',454,919),('x',455,1001),('y',456,1085),('z',456,1172)] if parent.endswith('before') else [('a',790,356),('b',794,470),('c',748,684),('d',786,752),('t',961,215),('u',995,299),('v',999,385),('w',1054,425),('x',997,555),('y',997,639),('z',997,721)]
    for label,x,y in positions:
        component(parent,'label-'+label,[x,y,x+25,y+27],f'External diagram label {label.upper()}.',kind='legend')

links=[]
def link(kind, left, right, reason):
    links.append(dict(kind=kind,left='ig2b07:'+left,right='ig2b07:'+right,reason=reason))
for group in [
 ['p25-842-intro','p25-842-b1','p25-842-b2','p25-842-b3','p25-842-b4','p25-842-b5','p25-842-b6','p25-842-tail'],
 ['p25-overview-intro','p25-overview1','p25-overview2','p25-overview3','p25-overview4','p25-overview5','p25-overview6'],
 ['p25-843-intro','p25-843-exempt-intro','p25-843-exempt1','p25-843-exempt2','p25-843-exempt3','p25-843-dr','p25-843-defender','p25-843-attacker','p25-843-all','p26-dr-mod-intro','p26-mod1','p26-mod2','p26-mod3','p26-mod4','p26-mod5','p26-mod6','p26-phalanx-exception','p26-pre-shock-close'],
 ['p26-845','p26-845-tail'],
 ['p26-step1','p26-position','p26-position-list','p26-position-b1','p26-position-b2','p26-position-b3','p26-position-b4','p26-position-tail','p26-weapon'],
 ['p26-step2','p26-step2-b1','p27-step2-b2','p27-srd-intro','p27-srd-b1','p27-srd-b2'],
 ['p27-step4','p27-result-b1','p27-result-b2','p27-result-b3','p27-result-b4','p27-result-tail'],
 ['p27-847','p27-collapse1','p27-collapse-ex1','p27-collapse2','p27-collapse-ex2','p27-collapse3','p27-engaged'],
 ['p28-charge-start','p28-charge-end'],['p28-struggle-b','exit-context']]:
    for left,right in zip(group,group[1:]):
        link('continuation',left,right,'Explicit paragraph/list/column/page sequence observed on the original assigned pages or permitted strip; structure only.')
for left,right in [('p25-play-note','entry-context'),('p25-design-note','entry-context'),('p26-play-note','p26-weapon'),('p27-design-note','p26-step2'),('p27-play-note','p27-847')]:
    link('note_for',left,right,'Visually associated note; no accepted semantic dependency asserted.')
for left,right in [('p25-example1','p25-842-intro'),('p25-example2','p25-842-intro'),('p26-example1','p26-845'),('p26-example2','p26-845'),('p26-example3','p26-845'),('p27-ratio-example','p26-step2'),('p27-leader-example','p27-step3'),('p28-diagram-before','p28-procedure'),('p28-diagram-after','p28-charge-start')]:
    link('illustrates',left,right,'Explicit example or diagram association observed; no gameplay legality inferred.')

cfg='private/workflow/orchestrator/20261016T195516Z-332903f5/002-IG-2B07-executor-78a83e6c/runtime-configuration.json'
author={'role':'executor','actor':'ig2:002-IG-2B07-executor-78a83e6c:executor','model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':cfg,'configuration_sha256':hashlib.sha256(Path(cfg).read_bytes()).hexdigest(),'format':'wgc-ig2b07-author-1','coordinate_basis':'Original full page 1224x1584 pixels at 144 DPI; integer floor conversion to page millionths. Adjacent boundaries share the same conversion.','regions':rows,'links':links,'limits':['All text remains machine-extracted, without a verified full transcription.','Inventory accounting is independent of KB headings; source semantics and executable readiness remain unprocessed.','Blank margins and gutters are explicit geometric gaps, not asserted semantic exclusions.','Nested artwork and diagram components can overlap each other and their parent; they have zero denominator contribution.']}
(A/'author-input.json').write_text(json.dumps(author,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'authored_regions':len(rows),'inventory':sum(r['role']=='inventory' for r in rows),'components':sum(r['category']=='component' for r in rows),'links':len(links)}))
