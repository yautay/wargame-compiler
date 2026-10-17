"""Explicit source-observed selections; coordinates measured on 1224x1584 originals.
No text, position, index or hash is used to allocate an identity. Keys below are
manual logical choices; UUIDs are allocated once and persisted by frozen assign.
"""
from ops import *
specs=[];links=[]
def add(page,key,kind,rect,label,components=None,uncertainty=None,group=None):
 specs.append({'page':page,'key':'ig2b02:'+key,'kind':kind,'observed_pixel_box':rect,'label':label,'components':components or [label],'uncertainty':uncertainty or [],'group':group or key})
def clause(p,key,rect,label,components=None):add(p,key,'clause',rect,label,components)
def full(p,key,y0,y1,label,kind='clause',right=False):
 add(p,key,kind,[628 if right else 88,y0,1137 if right else 597,y1],label)
def heading(p,key,y0,y1,label,right=False):full(p,key,y0,y1,label,'heading',right)
def wrapped(p,key,label,y0,split,y1,cy0,cy1,counter_labels,wide=False,right=False):
 x=628 if right else 88;tx=719 if right else (251 if wide else 179);end=1137 if right else 597
 add(p,key+':text-a','clause',[tx,y0,end,split],label+' (beside counter)',[label+' inline bold heading','Opening prose'],group=key)
 add(p,key+':counter','diagram',[x,cy0,x+(149 if wide else 77),cy1],label+' sample counter',counter_labels,uncertainty=['Small counter glyphs are literal observations; exact transcription and semantic interpretation remain pending.'],group=key)
 links.append(['illustrates','ig2b02:'+key+':counter','ig2b02:'+key+':text-a','Adjacent sample counter accompanies the named unit entry.'])
 if y1>split:
  add(p,key+':text-b','clause',[x,split+1,end,y1],label+' (below counter)',['Continued prose'],group=key)
  links.append(['continuation','ig2b02:'+key+':text-a','ig2b02:'+key+':text-b','Same printed paragraph wraps below its sample counter; geometric separation does not alter logical entry.'])
for p in (5,6,7,8):
 add(p,f'p{p}:running-header','editorial',[412,52,812,77],'SPQR running title and edition',['Italic/bold series title','Edition suffix'])
 add(p,f'p{p}:printed-label','editorial',[1122,47,1138,73] if p%2 else [88,47,103,74],f'Printed page label {p}')
 add(p,f'p{p}:header-rule','editorial',[88,78,1136,83],'Horizontal header rule')
 add(p,f'p{p}:copyright-footer','editorial',[522,1498,702,1521],'Copyright footer',['Copyright symbol','2026 GMT Games, LLC'])
full(5,'p5:triarii-authored-tail',105,155,'Triarii continuation from accepted page 4')
wrapped(5,'p5:alae','Alae Sociorum',164,260,525,171,247,['AS XIVa identifier (small glyph uncertain)','CO','J missile glyph','3','LG','6','5','Soldier illustration'])
full(5,'p5:maniple',535,657,'Maniple inline heading and paragraph')
wrapped(5,'p5:heavy-infantry','Heavy Infantry',666,762,811,672,748,['Aetolia','4','HO','5','HI','5','4','J missile glyph','Hoplite illustration'])
wrapped(5,'p5:phalanx','Phalanx',821,917,1206,827,903,['Macedon','6','PH','10','7','4','5','Phalanx soldier illustration'],wide=True)
wrapped(5,'p5:legion-infantry','Legion Infantry',1216,1312,1409,1222,1299,['I c','PR','J missile glyph','3','LG','8','5','Legionary and shield illustration'])
wrapped(5,'p5:medium-infantry','Medium Infantry',106,202,228,113,189,['Celts','12','J missile glyph','5','MI','5','5','Soldier illustration'],right=True)
wrapped(5,'p5:barbarian-infantry','Barbarian Infantry',237,333,455,243,320,['Gauls','5','5','BI','7','5','Soldier illustration'],right=True)
wrapped(5,'p5:light-infantry','Light Infantry',464,560,586,470,547,['Thrace','J missile glyph','5','LI','5','5','Soldier illustration'],right=True)
full(5,'p5:skirmishers',595,837,'Skirmishers inline heading and paragraph',right=True)
wrapped(5,'p5:javelinists','Javelinists',846,942,1016,852,929,['Thrace','J missile glyph','5','LI','5','5','Soldier illustration'],right=True)
wrapped(5,'p5:archers','Archers',1024,1120,1194,1031,1108,['Crete','A missile glyph','1','SK','4','6','Archer illustration'],right=True)
wrapped(5,'p5:slingers','Slingers',1203,1299,1373,1209,1286,["Bal'ric",'6','S missile glyph','1','SK','3','6','Slinger illustration'],right=True)
wrapped(5,'p5:light-cavalry','Light Cavalry',1382,1479,1479,1388,1465,['Nmdia','1','J missile glyph','4','LC','8','9','Mounted soldier illustration'],right=True)
full(6,'p6:light-cavalry-tail',105,155,'Light Cavalry continuation from page 5')
wrapped(6,'p6:lancers','Lancers',164,238,238,167,244,['Celts','5','4','LN','7','8','Mounted lancer illustration'])
wrapped(6,'p6:heavy-cavalry','Heavy Cavalry',255,351,377,262,338,['Crthge','Sndl','5','HC','7','8','Mounted soldier illustration'])
wrapped(6,'p6:roman-cavalry','Roman Cavalry',386,482,652,392,469,['Roman mounted javelinist illustration','3','RC','6','8','J missile glyph'])
wrapped(6,'p6:elephants','Elephants',661,757,1239,667,744,['Africa','15','J/a missile glyph (uncertain)','5','EL','5','7','Elephant/tower illustration'])
wrapped(6,'p6:scorpio','Scorpio',1248,1344,1394,1254,1331,['Scorpio','LI','1','2','3','Artillery illustration'])
heading(6,'p6:scale-heading',105,135,'2.5 GAME SCALE',True)
full(6,'p6:scale-hex-turn',136,186,'Hex distance and game-turn time',right=True)
full(6,'p6:scale-size',195,437,'Size scale and skirmisher exception',right=True)
full(6,'p6:scale-frontage',446,544,'Counter shape and frontage',right=True)
heading(6,'p6:length-heading',559,589,'2.6 GAME LENGTH',True)
full(6,'p6:length-withdrawal',590,640,'Battle duration and withdrawal',right=True)
full(6,'p6:length-turn-track',649,723,'Game Turn Track',right=True)
full(6,'p6:length-historical-note',727,906,'Historical note on duration and casualties','note',True)
heading(6,'p6:latin-heading',928,959,'2.7 LATIN',True)
full(6,'p6:latin-prose',960,1081,'Editorial Latin terminology discussion',right=True)
heading(6,'p6:sequence-heading',1110,1152,'3.0 SEQUENCE OF PLAY',True)
full(6,'p6:sequence-introduction',1153,1275,'Sequence of Play introduction',right=True)
heading(6,'p6:activation-heading',1289,1319,'A. Leader Activation Phase',True)
full(6,'p6:activation-prose',1321,1443,'Leader Activation Phase paragraph',right=True)
heading(7,'p7:orders-heading',105,135,'B. Orders Phase')
heading(7,'p7:movement-heading',140,166,'1. Movement and Missile Fire Segment')
full(7,'p7:movement-individual',167,217,'Movement segment item a: Individual Orders')
full(7,'p7:movement-line',220,270,'Movement segment item b: Line Commands')
full(7,'p7:movement-opponent',278,353,'Opponent withdrawal/extension/reaction paragraph')
heading(7,'p7:shock-heading',365,391,'2. Shock Combat Segment')
full(7,'p7:shock-introduction',392,442,'Shock Combat sequence introduction')
for key,y0,y1,label in [('designation',446,520,'a. Shock Designation'),('charge',522,548,'b. The Charge'),('leader-casualties',550,577,'c. Possible Leader Casualties'),('clash',579,629,'d. Clash of Spears and Swords'),('resolve',631,657,'e. Resolve the Shock'),('collapse-rout-pursuit',659,686,'f. Collapse, Rout, and Cavalry Pursuit')]:full(7,'p7:shock-'+key,y0,y1,label)
heading(7,'p7:momentum-heading',700,730,'C. Momentum Phase or Return to A')
full(7,'p7:momentum-prose',731,878,'Momentum paragraph')
heading(7,'p7:rout-reload-heading',892,922,'D. Rout and Reload Phase')
full(7,'p7:rout-movement',923,974,'1. Rout Movement')
full(7,'p7:reload',975,1026,'2. Reload Segment')
full(7,'p7:flip-remove',1027,1102,'3. Flip and Remove')
heading(7,'p7:withdrawal-heading',1116,1146,'E. Withdrawal Phase')
full(7,'p7:withdrawal-prose',1147,1270,'Withdrawal paragraph')
heading(7,'p7:leaders-heading',107,148,'4.0 LEADERS',True)
full(7,'p7:leaders-introduction',149,270,'Leader orders and counter sides',right=True)
add(7,'p7:sample-leader-diagram','diagram',[698,278,1055,431],'Sample Leader Counter annotated diagram',['Sample Leader Counter caption','P. Scipio counter and portrait','Name callout','Elite Initiative Indicator callout/arrow and triangle','Command Range callout/arrow to 8','Initiative callout/arrow to 6','Line Command Rating callout/arrow to 2','Charisma callout/arrow to boxed 3','Strategy Rating callout/arrow to red 7'],group='p7:sample-leader')
heading(7,'p7:leader-counters-heading',455,484,'4.1 LEADER COUNTERS',True)
full(7,'p7:ratings-introduction',486,513,'Leader ratings introduction',right=True)
for key,y0,y1,label in [('command-range',521,620,'Command Range'),('elite-commander',628,679,'Elite Commander and red triangle'),('initiative',687,833,'Initiative'),('line-command',841,940,'Line Command'),('strategy',948,999,'Strategy'),('charisma',1007,1106,'Charisma'),('movement-allowance',1274,1397,'Movement Allowance'),('command-restriction',1405,1480,'Command Restriction')]:full(7,'p7:rating-'+key,y0,y1,label+' inline heading and paragraph',right=True)
full(7,'p7:charisma-design-note',1109,1263,'Design note on Charisma','note',True)
links.append(['note_for','ig2b02:p7:charisma-design-note','ig2b02:p7:rating-charisma','Shaded DESIGN NOTE follows the Charisma paragraph.'])
links.append(['illustrates','ig2b02:p7:sample-leader-diagram','ig2b02:p7:leaders-introduction','Annotated leader counter accompanies the introductory explanation of leader counters.'])
heading(8,'p8:individual-heading',105,164,'4.2 LEADER CAPABILITIES: INDIVIDUAL ORDERS')
full(8,'p8:individual-range',165,288,'4.21 Command Range introduction')
for key,y0,y1,label in [('enemy-unit',291,317,'4.21 bullet: enemy occupied hex'),('enemy-zoc',318,344,'4.21 bullet: enemy ZOC'),('terrain',345,371,'4.21 bullet: impassable terrain')]:full(8,'p8:path-'+key,y0,y1,label)
full(8,'p8:range-calculation',379,454,'4.21 Friendly unit negation and instant range calculation')
for key,y0,y1,label in [('individual-effects',462,585,'4.22 IO actions/count/Finished side'),('leader-movement',593,715,'4.23 Leader movement'),('enemy-zoc-orders',724,870,'4.24 Enemy ZOC and OC'),('finished-leader',878,929,'4.25 Finished leader')]:full(8,'p8:'+key,y0,y1,label)
heading(8,'p8:line-heading',943,974,'4.3 LEADER CAPABILITIES: LINE COMMANDS')
full(8,'p8:line-orders',975,1217,'4.31 Line Commands')
full(8,'p8:line-composition-left',1225,1468,'4.32 Line Composition left-column paragraph')
full(8,'p8:line-composition-right',105,277,'4.32 continuation at top of right column',right=True)
full(8,'p8:cannae-example',284,431,'Cannae deployment EXAMPLE','example',True)
full(8,'p8:line-historical-note',436,589,'Historical note on scenario line adjustments','note',True)
full(8,'p8:line-eligibility',606,849,'4.33 Line Command Eligibility',right=True)
heading(8,'p8:overall-heading',861,888,'Overall Commanders',True)
full(8,'p8:overall-prose',889,939,'Overall Commanders paragraph',right=True)
heading(8,'p8:subordinate-heading',951,978,'Subordinate Commanders',True)
full(8,'p8:subordinate-introduction',979,1029,'Subordinate Commanders introduction',right=True)
full(8,'p8:subordinate-condition-one',1032,1083,'Condition 1 including printed or',right=True)
full(8,'p8:subordinate-condition-two',1085,1207,'Condition 2 die roll and modifiers',right=True)
full(8,'p8:exception-one',1215,1266,'Exception #1',right=True)
full(8,'p8:exception-two',1274,1324,'Exception #2',right=True)
full(8,'p8:subordinate-momentum',1333,1431,'Momentum-generated Orders Phase paragraph',right=True)
links.extend([
 ['continuation','ig2b02:p5:light-cavalry:text-a','ig2b02:p6:light-cavalry-tail','Printed hyphenated magnifi- / cent continues across pages 5 and 6.'],
 ['continuation','ig2b02:p8:line-composition-left','ig2b02:p8:line-composition-right','Rule 4.32 continues from bottom left to top right of the same physical page.'],
 ['note_for','ig2b02:p6:length-historical-note','ig2b02:p6:length-turn-track','Shaded historical note follows section 2.6.'],
 ['note_for','ig2b02:p8:cannae-example','ig2b02:p8:line-composition-right','Printed EXAMPLE follows Line Composition continuation.'],
 ['note_for','ig2b02:p8:line-historical-note','ig2b02:p8:line-composition-right','Historical note follows Line Composition example.'],
 ['continuation','ig2b01:p4:triarii-text-a','ig2b02:p5:triarii-authored-tail','Accepted pinned page-4 Triarii crop ends spear-armed; independently observed page-5 paragraph begins heavy infantry. Old context continuation remains unchanged.']])
# Explicit grouping and reading order: running furniture first, then left column
# top-to-bottom with text beside a counter before the counter and wrapped remainder,
# then right column; footer last. This orders references, never assigns identities.
orders={}
for p in (5,6,7,8):
 editorial={s['key'].split(':')[-1]:s for s in specs if s['page']==p and s['kind']=='editorial'}
 body=[s for s in specs if s['page']==p and s['kind']!='editorial']
 # Source-observed column reading order; stable explicit specification keys retained.
 body.sort(key=lambda s:(s['observed_pixel_box'][0]>=620,s['observed_pixel_box'][1],s['kind']=='diagram'))
 orders[str(p)]=[editorial[x]['key'] for x in ('running-header','printed-label','header-rule')]+[s['key'] for s in body]+[editorial['copyright-footer']['key']]
write('author-specifications-final.json',{'coordinate_measurement':'Manual rectangles on exact 144-DPI 1224x1584 original PNGs; outward integer normalization; keys are explicit logical choices, never generated from measurement.','specifications':specs,'page_order_keys':orders,'links':links,'grouping_policy':'Inline bold entry headings/rule numbers and prose share a clause region; counters retain illustration/text/rating components in one diagram region; wrapped prose has linked disjoint new regions. Every grouping is an initial authored composition, not a split/merge of accepted inventory identities. No acceptance transfer.','page_9_access':'Not needed: final page-8 paragraph is syntactically complete. No page-9 content accessed.'})
print('Explicit specifications:',len(specs))
