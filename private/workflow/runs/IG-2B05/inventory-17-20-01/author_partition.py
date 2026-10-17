"""Fresh author partition from original assigned 144-DPI page inspection.

Coordinates below address the 1224 x 1584 original page rasters, top-left.
They are explicit author boundaries, never inferred from KB headings or text flow.
"""
from pathlib import Path
import json

ROOT = Path(__file__).parent
ROWS = []

def add(page, key, kind, box, title, components=None):
    ROWS.append(dict(page=page, key=f'physical-page:{page}:ig2b05:{key}',
                     kind=kind, pixel_box=box, title=title,
                     components=components or [title]))

def left(page, key, kind, top, bottom, title, components=None):
    add(page,key,kind,[88,top,596,bottom],title,components)

def right(page, key, kind, top, bottom, title, components=None):
    add(page,key,kind,[628,top,1136,bottom],title,components)

for page in (17,18,19,20):
    add(page,'running-header','editorial',[88,44,1136,83],
        'Running title, edition, printed page glyph and horizontal rule',
        ['Running title and edition','Printed page glyph (not verified page-label metadata)','Horizontal rule'])

left(17,'6-56','clause',102,222,'6.56 Orderly Withdrawal timing and moving-unit continuation')
left(17,'6-56-exception','clause',233,330,'6.56 Rampaging Elephant exception')
left(17,'withdrawal-example','example',340,845,'Example of Withdrawal',
     ['Example heading','Cannae cavalry and Velites setup','Phalanx approach and repeated withdrawals','Cohesion-hit observations','Final remaining-MP sentence'])
left(17,'withdrawal-play-note','note',853,982,'Withdrawal example play note (gray panel)')
left(17,'6-57','clause',990,1234,'6.57 Cavalry Line Withdrawal',
     ['Numbered heading','Eligibility and collective withdrawal text','Individual OW consequence'])
right(17,'6-6-heading','heading',103,132,'6.6 Stacking')
right(17,'stacking-introduction','clause',134,446,'Stacking introductory definitions and Roman color borders')
right(17,'stacking-design-note','note',453,607,'Stacking design note (blue panel)')
right(17,'6-61','clause',615,809,'6.61 Basic, non-Roman Stacking Rule')
right(17,'6-62','clause',818,868,'6.62 Enemy-occupied hex prohibition')
right(17,'6-62-exception','clause',873,901,'6.62 Elephant Pass-Thru exception')
right(17,'6-63','clause',908,1031,'6.63 Stacking Chart introduction and terminology')
right(17,'6-63-basic','clause',1032,1083,'6.63 Basic bullet')
right(17,'6-63-color','clause',1084,1159,'6.63 Different Color bullet')
right(17,'6-63-class','clause',1160,1187,'6.63 Different Class bullet')
right(17,'6-63-roman','clause',1188,1285,'6.63 Roman bullet')
right(17,'stacking-play-note','note',1290,1397,'Stacking chart play note (gray panel)')
right(17,'voluntary-example-start','example',1405,1479,'Example 1 (Voluntary), beginning continued on page 18')

left(18,'voluntary-example-velites','example',102,199,'Example 1 continuation: Velites')
left(18,'voluntary-example-hastati','example',209,403,'Example 1 continuation: Hastati')
left(18,'rout-retreat-example','example',411,725,'Example 2 (Rout/Retreat)',
     ['Example heading','Routed Velites illustration','Stationary-unit die-roll passage','Hastati and stopping-in-occupied-hex passages'])
left(18,'roman-flexibility-note','note',733,1054,'Roman flexibility design note (blue panel)')
left(18,'6-64','clause',1063,1185,'6.64 Moving stacked units by orders')
left(18,'6-65','clause',1194,1291,'6.65 Leader and combat-unit stacking')
left(18,'6-66-start','clause',1300,1475,'6.66 Stacking-order change and entry, beginning')
right(18,'6-66-end','clause',102,151,'6.66 Entry Reaction Fire and Shock-marker continuation')
right(18,'6-67','clause',160,282,'6.67 Stacked facing alignment')
right(18,'6-68','clause',291,319,'6.68 Stacking effects introduction')
right(18,'6-68-size','clause',321,372,'6.68 Size bullet')
right(18,'6-68-missile','clause',373,399,'6.68 Top-unit Missile Fire bullet')
right(18,'6-68-enemy-missile','clause',400,475,'6.68 Enemy Missile Fire bullet')
right(18,'6-68-tq','clause',476,550,'6.68 Individual TQ-check bullet')
right(18,'6-68-drm','clause',551,577,'6.68 Stacked-unit DRM bullet')
right(18,'6-68-cohesion','clause',578,674,'6.68 Shock Cohesion Hits bullet')
right(18,'6-68-rout','clause',675,725,'6.68 Rout propagation bullet')
right(18,'6-69','clause',732,807,'6.69 The Stacking Chart')
right(18,'6-7-heading','heading',821,851,'6.7 Column Movement')
right(18,'column-design-note','note',852,1054,'Column movement design note (blue panel)')
add(18,'in-column-marker','diagram',[628,1064,707,1146],'In Column marker',
    ['White marker face with dot pattern','Magenta arrow','Black lower field and yellow In Column label'])
add(18,'6-71-upper','clause',[719,1062,1136,1160],'6.71 Column formation, text beside marker')
right(18,'6-71-lower','clause',1161,1234,'6.71 Column formation, text below marker')
right(18,'6-71-exceptions','clause',1236,1289,'6.71 BI, SK and routed-unit exceptions')
right(18,'6-72','clause',1294,1417,'6.72 In Column MA and terrain costs')
right(18,'6-73-start','clause',1424,1475,'6.73 In Column facing, beginning continued on page 19')

left(19,'6-73-end','clause',102,391,'6.73 In Column facing, continuation')
left(19,'6-74','clause',400,667,'6.74 Front and front-flank movement')
left(19,'column-diagram','diagram',675,868,'Phalanx Column front-flank movement diagram',
     ['Two rows of hex outlines','Opaque red Phalanx counter with In Column marker','Translucent destination counter and marker','Green curved arrow and white directional arrow'])
left(19,'column-caption','legend',870,896,'Phalanx Column movement caption')
left(19,'6-75','clause',902,1049,'6.75 Column TQ, attacks, Recovery and superiority')
left(19,'6-76','clause',1056,1203,'6.76 Shock attack and non-column formation')
left(19,'6-77','clause',1210,1333,'6.77 Column withdrawal, movement-through and rout')
right(19,'6-8-heading','heading',101,132,'6.8 Pre-arranged Withdrawal')
add(19,'prearranged-marker','diagram',[628,140,706,219],'Pre-Arranged Withdrawal marker',
    ['Outlined square','Blue field','Pre-Arranged Withdrawal label'])
add(19,'no-pw-marker','diagram',[709,140,788,219],'NO PW marker',
    ['Outlined square','Red NO field','Black PW label'])
add(19,'pw-introduction-upper','clause',[800,134,1136,231],'PW introduction, text beside markers')
right(19,'pw-introduction-lower','clause',232,281,'PW introduction, text below markers')
right(19,'6-81','clause',287,507,'6.81 PW leader, infantry line and Momentum limits')
right(19,'6-82','clause',513,732,'6.82 PW designation and marker placement')
right(19,'6-83','clause',739,839,'6.83 Revealing the marker and event-order introduction')
right(19,'6-83-withdrawal','clause',841,1041,'6.83 Infantry-approach withdrawal bullet')
right(19,'6-83-leader','clause',1042,1138,'6.83 Leader-activation bullet')
right(19,'pw-play-note-1','note',1143,1219,'PW Play Note 1')
right(19,'pw-play-note-2','note',1226,1374,'PW Play Note 2')

left(20,'7-0-heading','heading',102,145,'7.0 Facing and ZOCs (blue heading)')
left(20,'7-1-heading','heading',150,179,'7.1 Facing')
left(20,'7-11','clause',180,352,'7.11 Facing and Front/Flank/Rear hexes')
add(20,'single-hex-facing','diagram',[238,373,443,502],'Single-hex unit facing diagram',
    ['Hex outline','One-hex combat counter','Two Front labels','Two Flank labels','Two Rear labels'])
add(20,'phalanx-facing','diagram',[190,525,492,653],'Phalanx facing diagram',
    ['Double-width counter and hex outlines','Three Front labels','Two Flank labels','Three Rear labels'])
left(20,'7-12','clause',672,724,'7.12 Pivot and MP introduction')
left(20,'7-12-roman','clause',726,800,'7.12 Roman infantry bullet')
left(20,'7-12-elephant','clause',801,851,'7.12 Elephant bullet')
left(20,'7-12-skirmisher','clause',852,879,'7.12 Skirmisher bullet')
left(20,'7-12-column','clause',880,907,'7.12 Column-reference bullet')
left(20,'7-13','clause',912,988,'7.13 Phalanx movement and pivot')
left(20,'7-14','clause',994,1142,'7.14 Rough-terrain facing change')
left(20,'7-15','clause',1150,1444,'7.15 Reaction Facing Change')
right(20,'7-15-exception','clause',101,176,'7.15 Cavalry exception (same-page column continuation)')
right(20,'7-15-play-note','note',183,241,'7.15 Stacked-unit play note (gray panel)')
right(20,'7-16','clause',248,348,'7.16 Reverse Face reaction')
right(20,'reverse-face-note','note',354,438,'Reverse Face design note (blue panel)')
right(20,'7-2-heading','heading',450,482,'7.2 Zones of Control (ZOC)')
add(20,'zoc-introduction','clause',[628,483,908,584],'ZOC definition beside diagram')
add(20,'zoc-diagram','diagram',[911,484,1136,700],'Zones of Control diagram',
    ['Central unit counter','Two yellow Front ZOC hexes with labels','Two Flank hexes with labels','Two Rear hexes with labels'])
add(20,'7-21-upper','clause',[628,589,908,712],'7.21 ZOC extent, text beside diagram')
right(20,'7-21-lower','clause',713,811,'7.21 ZOC extent, text below diagram')
right(20,'7-22','clause',816,868,'7.22 Prohibited-movement hexes')
right(20,'7-23','clause',876,951,'7.23 Entering or leaving enemy ZOC introduction')
right(20,'7-23-combat-unit','clause',953,1076,'7.23 Combat-unit movement bullet')
right(20,'7-23-oc','clause',1077,1104,'7.23 OC Individual Order bullet')
right(20,'7-23-leader','clause',1105,1157,'7.23 Leader two-orders bullet')
right(20,'7-23-exception','clause',1161,1214,'7.23 Non-Shock-capable enemy exception')
right(20,'7-23-play-note','note',1219,1278,'7.23 Skirmisher play note (gray panel)')
right(20,'7-23-following','clause',1284,1361,'7.23 Entering another enemy ZOC')
right(20,'7-24-start','clause',1367,1467,'7.24 Beginning in enemy ZOC, unfinished at page-20 exit')

for page in (17,18,19,20):
    add(page,'copyright-footer','editorial',[520,1494,708,1520],'Copyright footer')

# Explicit margins refined against the assigned pages' glyph bounds. These do not
# change component membership. Touching edges are half-open, never overlapping.
BOTTOMS = {
    17: {'6-56':226,'6-56-exception':332,'withdrawal-example':847,'6-57':1235,
         '6-6-heading':133,'stacking-introduction':448,'6-61':811,'6-62':870,
         '6-63-basic':1085,'voluntary-example-start':1480},
    18: {'voluntary-example-velites':202,'voluntary-example-hastati':404,
         'rout-retreat-example':727,'6-64':1187,'6-65':1293,'6-66-end':154,
         '6-67':284,'6-68-size':373,'6-68-missile':400,'6-68-cohesion':675,
         '6-68-rout':726,'6-69':809,'6-7-heading':854,'6-71-upper':1161,
         '6-72':1418,'6-73-start':1477},
    19: {'6-73-end':394,'6-74':668,'6-75':1050,'6-76':1205,'6-77':1336,
         '6-8-heading':133,'pw-introduction-upper':232,'6-82':733,'6-83':840},
    20: {'7-0-heading':148,'7-1-heading':182,'7-11':353,'phalanx-facing':655,
         '7-12':725,'7-12-roman':802,'7-12-elephant':853,'7-12-skirmisher':880,
         '7-13':989,'7-14':1144,'7-15-exception':178,'7-16':349,
         '7-2-heading':483,'7-21-upper':714,'7-22':869,'7-23':952,
         '7-23-combat-unit':1078,'7-23-oc':1105,'7-24-start':1468},
}
TOPS = {17:{'6-63-color':1085},18:{'column-design-note':854},
        20:{'7-11':182,'7-12-elephant':802,'7-12-skirmisher':853,
            '7-21-lower':714,'7-23-oc':1078}}
for row in ROWS:
    key=row['key'].split(':')[-1]
    if key in BOTTOMS.get(row['page'],{}):
        row['pixel_box'][3]=BOTTOMS[row['page']][key]
    if key in TOPS.get(row['page'],{}):
        row['pixel_box'][1]=TOPS[row['page']][key]

if __name__ == '__main__':
    output={'format':'wgc-authored-partition-1','task':'IG-2B05',
            'basis':'Fresh full original-page visual inspection; explicit author boundaries.',
            'pixel_frame':{'width':1224,'height':1584,'dpi':144,'origin':'top-left'},
            'regions':ROWS,
            'context_only_accesses':[],
            'uncertainty':['Machine text is not verified transcription.',
                           'Component names describe visible structure and do not decide gameplay legality.',
                           'Blank geometric gaps remain explicit; no exclusion is authorized.',
                           'Adjacent pages 16 and 21 were not inspected.']}
    path=ROOT/'authored-partition.json'
    with path.open('w',encoding='utf-8',newline='\n') as f:
        f.write(json.dumps(output,indent=2,ensure_ascii=True)+'\n')
    print(f'Authored {len(ROWS)} disjoint candidate regions.')
