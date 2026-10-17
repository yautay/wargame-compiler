from prepare import *
from math import floor,ceil
tool=read(f'{REL}/toolchain.json'); sys.path[:0]=tool['process_pythonpath'].split(';'); os.environ['PATH']=tool['process_path_prefix']+';'+os.environ['PATH']; os.environ['PYTHONDONTWRITEBYTECODE']='1'
from wgc.sources.inventory import make_region, assemble, seal, validate, digest
from wgc.sources.pdf import extract_evidence
from wgc.contracts.source import canonical_bytes

spec=[]
def add(p,key,kind,box,label,components=None,uncertainty=None):
 spec.append({'page':p,'key':'ig2b01:'+key,'kind':kind,'native_top_left_points':box,'label':label,'components':components or [],'uncertainty':uncertainty or []})
def col(p,key,kind,y0,y1,label,right=False,**kw): add(p,key,kind,[313 if right else 43,y0,569 if right else 299,y1],label,**kw)
def furniture(p):
 add(p,f'p{p}:running-header','editorial',[200,23,409,39],'Running series/edition header')
 add(p,f'p{p}:folio','editorial',[44 if p%2==0 else 560,23,54 if p%2==0 else 569,38],f'Printed page {p}')
 add(p,f'p{p}:header-rule','editorial',[44,39,568,41],'Horizontal header rule')
 add(p,f'p{p}:copyright','editorial',[260,747,352,761],'Copyright footer')

# Cover, including source extraction artifacts invisible under the opaque cover.
add(1,'cover:hidden-running-template','editorial',[43,23,569,42],'Underlying running header and folio; not visible in rendered cover',uncertainty=['Extracted text layer includes a hidden running header and folio 1; this is not a visible printed cover label.'])
add(1,'cover:series','heading',[98,50,514,73],'Series and volume line')
add(1,'cover:spqr-logotype','heading',[186,82,412,155],'SPQR logotype',uncertainty=['Large SPQR lettering is visible as artwork/vector outlines but absent from extracted text; PNG is required.'])
add(1,'cover:subtitle','heading',[112,158,501,183],'Roman Republic subtitle')
add(1,'cover:artwork','diagram',[131,187,479,487],'Cover battle illustration and its white frame',components=['Battle artwork','White illustration frame'])
add(1,'cover:design-credit','editorial',[178,497,437,516],'Designer credit')
add(1,'cover:rulebook-title','heading',[148,519,465,566],'Rule Book title')
add(1,'cover:edition','heading',[270,567,344,587],'5th Edition')
add(1,'cover:toc-heading','heading',[242,601,369,620],'Table of Contents heading')
for side,items in enumerate([['Introduction','Game Components and Terminology','The Sequence of Play','Leaders','Leader Activation and Orders','Movement'],['Facing and ZOCs','Combat','Special Combat Units','The Effects of Combat','Army Withdrawal and Victory','Rules Index']]):
 for i,label in enumerate(items):
  add(1,f'cover:toc:{"left" if side==0 else "right"}:{i+1}','editorial',[61 if side==0 else 313,626+16*i,294 if side==0 else 546,641+16*i],'TOC entry: '+label,components=['Section label/name','Dot leader','Printed destination number; unresolved navigation, no target content inspected'])
add(1,'cover:toc-frame-top','editorial',[44,597,568,599],'TOC panel upper rule')
add(1,'cover:toc-frame-left','editorial',[44,599,46,731],'TOC panel left rule')
add(1,'cover:toc-frame-right','editorial',[566,599,568,731],'TOC panel right rule')
add(1,'cover:toc-frame-bottom','editorial',[44,730,568,732],'TOC panel lower rule',uncertainty=['Panel corner rules touch at half-open boundaries; no semantic exclusion inferred.'])
# avoid corner overlap: vertical rules stop before lower horizontal rule
for s in spec:
 if s['key'] in ['ig2b01:cover:toc-frame-left','ig2b01:cover:toc-frame-right']: s['native_top_left_points'][3]=730
add(1,'cover:publisher-address','editorial',[184,746,429,762],'Visible publisher/address footer and overlapping hidden copyright text',uncertainty=['Text extraction interleaves invisible copyright and visible address; raw text retained without repair.'])

furniture(2)
col(2,'p2:introduction-title','heading',52,74,'1.0 Introduction')
for key,kind,a,b,label in [('intro-opening','clause',74,147,'Introduction: scope and period'),('intro-systems','clause',151,368,'Introduction: historical systems and Scipio'),('intro-notes','clause',372,470,'Introduction: historical notes and player experience'),('edition-note','note',474,560,'5th Edition Note'),('player-note','note',563,673,'Note to Players'),('new-player-note-a','note',677,740,'For Those Who Have Not Played: first column fragment')]: col(2,'p2:'+key,kind,a,b,label)
col(2,'p2:new-player-note-b','note',52,127,'For Those Who Have Not Played: second column completion',True)
col(2,'p2:components-title','heading',140,179,'2.0 Game Components and Terminology',True)
col(2,'p2:components-intro','clause',179,193,'Components list introduction',True)
for key,a,b,label in [('maps',194,207,'Six map sheets'),('counters',208,220,'Six counter sheets'),('rulebook',221,234,'Rulebook'),('scenario-i',235,247,'Scenario Book I'),('scenario-ii',248,261,'Scenario Book II'),('scenario-iii',262,274,'Scenario Book III'),('player-aids',275,300,'Player aid cards and copies'),('tracking-card',301,313,'Rout Point Tracking/Game Turn Card'),('die',314,327,'Ten-sided die'),('bags',328,341,'Storage bags')]: col(2,'p2:component:'+key,'clause',a,b,label,True)
for key,kind,a,b,label in [('maps-title','heading',347,363,'2.1 The Maps'),('maps-body','clause',363,425,'Map/hex-grid description'),('pieces-title','heading',431,446,'2.2 The Playing Pieces'),('pieces-intro','clause',447,497,'Three types of playing pieces'),('combat-units','clause',500,634,'2.21 Combat units, ratings, missiles, reverse side'),('types-classes','clause',638,699,'2.22 Types and classes; examples retained within clause'),('legions-a','clause',703,741,'2.23 The Legions: page 2 fragment')]: col(2,'p2:'+key,kind,a,b,label,True)

furniture(3)
col(3,'p3:legions-b','clause',52,163,'2.23 continuation: historical numbering and skill introduction')
for key,a,b,label in [('elite',166,179,'Crack/Elite'),('veteran',180,193,'Veteran'),('standard',194,206,'Standard'),('recruits',207,220,'Recruits')]: col(3,'p3:skill:'+key,'clause',a,b,'Legion skill bullet: '+label)
for key,kind,a,b,label in [('legion-marking','clause',224,262,'Legion and alae number examples'),('legion-border','clause',265,303,'Legion/ala border colors'),('legion-units','clause',307,524,'2.24 Legion Units: historical note and adjustment suggestion'),('leaders','clause',528,554,'Leaders ratings; raw reference 4.1'),('markers','clause',558,608,'Information markers and printed marker examples')]: col(3,'p3:'+key,kind,a,b,label)
add(3,'p3:examples-heading','heading',[322,66,557,83],'2.25 Examples of Combat Units')
add(3,'p3:diagram:phalanx','diagram',[322,85,557,163],'Double-sized infantry (Phalanx) annotated example',components=['Double-sized Infantry (Phalanx) caption','Counter artwork and every printed counter value','Unit Name/ID','Unit Type','Extended Movement Allowance','Movement Allowance','Size','Troop Quality','All leader lines'])
add(3,'p3:diagram:infantry','diagram',[322,171,557,248],'Two infantry counters and shared annotation',components=['Infantry caption','Both counter images and values','Unit Name/ID connector to both counters','Unit Class','Type of Missile','Unit Type','Movement Allowance','Troop Quality (TQ)','Size','All leader lines'])
add(3,'p3:diagram:cavalry','diagram',[322,253,557,332],'Two cavalry counters and shared annotation',components=['Cavalry caption','Both counter images and values','Unit Name/ID','Type of Missile','Unit Type','Movement Allowance','Troop Quality (TQ)','Unit Class','Size','All leader lines'])
add(3,'p3:diagram:scorpion','diagram',[322,340,432,397],'Scorpion counter and legend',components=['Scorpion caption','Counter image/values','Unit Type','Range','Leader lines'])
add(3,'p3:diagram:elephant','diagram',[434,340,557,397],'Elephant counter and legend',components=['Elephant caption','Counter image/values','Archer Screen','Type of Missile','Leader lines'])
for key,x0,x1,caption in [('camel',323,365,'Camel'),('archer',374,413,'Archer'),('chariot',422,461,'Chariot'),('leader',470,510,'Leader'),('elephant-leader',520,560,'Elephant Leader')]:
 add(3,'p3:sample:'+key,'diagram',[x0,408,x1,469],caption+' sample counter and caption',components=['Complete counter artwork and embedded labels/numbers/symbols',caption+' caption'])
add(3,'p3:panel-top','editorial',[314,53,568,55],'Examples panel top border')
add(3,'p3:panel-left','editorial',[314,55,316,476],'Examples panel left border')
add(3,'p3:panel-right','editorial',[566,55,568,476],'Examples panel right border')
add(3,'p3:panel-bottom','editorial',[314,476,568,478],'Examples panel bottom border')
for key,kind,a,b,label in [('charts-title','heading',489,505,'2.3 Charts, Tables and the Die'),('charts-body','clause',505,531,'Chart/table usage and die zero convention'),('terminology-title','heading',537,553,'2.4 Terminology'),('terminology-intro','clause',553,579,'Terminology introduction'),('term-active-leader','clause',583,609,'Active Leader definition'),('term-class','clause',612,650,'Class definition with inline example'),('term-cohesion','clause',653,691,'Cohesion definition'),('term-depletion','clause',695,720,'Depletion definition'),('term-dr','clause',724,738,'DR definition')]: col(3,'p3:'+key,kind,a,b,label,True)

furniture(4)
for key,a,b,label in [('drm',52,67,'DRM'),('finished-leader',70,120,'Finished Leader'),('inactive-leader',124,149,'Inactive Leader'),('leader',153,191,'Leader'),('line',195,232,'Line'),('ma',236,274,'MA'),('missile-fire',278,303,'Missile Fire'),('momentum',307,332,'Momentum'),('mp',336,350,'MP'),('order-line-command',354,440,'Order/Line Command'),('orders-phase',443,469,'Orders Phase'),('shock-combat',473,498,'Shock Combat'),('size',502,564,'Size'),('superiority',568,618,'Superiority'),('tq',621,683,'TQ and chart reference 8.75'),('trump',686,737,'Trump')]: col(4,'p4:term:'+key,'clause',a,b,label+' definition')
for key,a,b,label in [('type',52,91,'Type definition with examples'),('zoc',95,132,'Zone of Control definition'),('combat-types-intro',136,162,'Combat unit types/terms introduction'),('consular-army',165,348,'Consular Army description'),('legion',351,413,'Legion description')]: col(4,'p4:'+key,'clause',a,b,label,True)
add(4,'p4:velites-text','clause',[359,416,569,467],'Velites description')
add(4,'p4:velites-counter','diagram',[313,417,353,458],'Velites illustrated counter',components=['Counter image and all printed values/symbols'])
add(4,'p4:hastati-text-a','clause',[359,470,569,518],'Hastati description alongside counter')
add(4,'p4:hastati-counter','diagram',[313,471,353,512],'Hastati illustrated counter',components=['Counter image and all printed values/symbols'])
col(4,'p4:hastati-text-b','clause',518,628,'Hastati description continued below counter',True)
add(4,'p4:principes-text-a','clause',[359,631,569,679],'Principes description alongside counter')
add(4,'p4:principes-counter','diagram',[313,632,353,673],'Principes illustrated counter',components=['Counter image and all printed values/symbols'])
col(4,'p4:principes-text-b','clause',679,693,'Principes description final line',True)
add(4,'p4:triarii-text-a','clause',[359,696,569,735],'Triarii description; continues at physical page 5')
add(4,'p4:triarii-counter','diagram',[313,697,353,738],'Triarii illustrated counter',components=['Counter image and all printed values/symbols'])

def build(registry):
 b=read(f'{BASE}/inventory-one/inventory.json'); pages=copy.deepcopy(b['pages']); regions=[]; ledger=[]
 for s in spec:
  page=pages[s['page']-1]; x0,y0,x1,y1=s['native_top_left_points']; box=[floor(x0/612*1e6),floor(y0/792*1e6),floor(x1/612*1e6),floor(y1/792*1e6)]
  r=make_region(registry,s['key'],page,box,kind=s['kind'],reason='Authored source inventory; raw extraction/PNG retained. Exact transcription and source-IG reconciliation remain pending.')
  r['uncertainty']=s['uncertainty']+(['Embedded counter text/symbols are not reliably available in extraction; inspect PNG and retain a transcription gap.'] if s['kind']=='diagram' else [])
  r['coverage']['transcription']={'status':'partial','gap':True,'reason':'Literal extracted text and image are retained separately; no independently verified full transcription or source-IG binding.','boundary':None}
  r=seal(r); regions.append(r); ledger.append({**s,'region_id':r['id'],'region_revision':r['revision'],'box':box,'denominator_role':'inventory','exact_native_bbox_basis':'Authored PDF-point top-left bounds quantized down to integer page millionths at every edge. Shared edges use the identical integer, preserving half-open disjointness. These exact normalized bounds are authoritative; evidence uses their rational inverse, not rounded display points.','content_inventory_status':'authored; independent review pending','semantic_acceptance':False})
 ctx=read(f'{REL}/context-record.json')['region']; ctx['box'][3]=ceil(78/792*1e6); ctx['uncertainty']=['Only the two-line Triarii completion at page 5 top left; no neighboring entry included.']; ctx=seal(ctx)
 # preserve assigned context UUID through persisted registry replay
 assert any(e['id']==ctx['id'] for e in registry['entries'])
 regions += [copy.deepcopy(r) for r in b['regions'] if int(r['key'].split(':')[1])>=5]
 regions.append(ctx)
 by={r['key']:r['id'] for r in regions}; links=[]
 def link(a,z,reason,kind='continuation'): links.append({'kind':kind,'from':by['ig2b01:'+a],'to':by['ig2b01:'+z],'reason':reason})
 for a,z,reason in [('p2:new-player-note-a','p2:new-player-note-b','Same player note across columns, left bottom to right top.'),('p2:legions-a','p3:legions-b','2.23 sentence crosses physical pages 2 to 3.'),('p3:term-dr','p4:term:drm','Terminology list continues across physical pages 3 to 4; separate entries, not one sentence.'),('p4:hastati-text-a','p4:hastati-text-b','Paragraph wraps around the illustrated counter.'),('p4:principes-text-a','p4:principes-text-b','Paragraph wraps around the illustrated counter.'),('p4:triarii-text-a','context:triarii-tail','Incomplete Triarii sentence completes in the exact two-line page 5 context crop.')]: link(a,z,reason)
 for key in ['phalanx','infantry','cavalry','scorpion','elephant']: link('p3:diagram:'+key,'p3:examples-heading','Annotated counter and all legends belong to the 2.25 examples panel.','illustrates')
 for key in ['velites','hastati','principes','triarii']: link('p4:'+key+'-counter','p4:'+key+'-text'+('' if key=='velites' else '-a'),'Adjacent illustrated unit sample.','illustrates')
 # Explicit reader order: furniture is separately placed before/after each page's content.
 order=[]
 for p in range(1,5):
  rows=[r for r in regions if r['page_id']==pages[p-1]['id']]
  # spec is explicitly authored in left-column then right-column order; panel frames are last in panel.
  order.extend(r['id'] for r in rows if not r['key'].endswith(':copyright'))
  order.extend(r['id'] for r in rows if r['key'].endswith(':copyright'))
 order.append(ctx['id']); order.extend(r['id'] for r in regions if r['key'].endswith('unprocessed-placeholder'))
 doc=assemble(b['source'],pages,regions,registry,reading_order=order,links=links,toolchain=b['toolchain'])
 return doc,ledger

if __name__=='__main__':
 registry=read(f'{REL}/context-record.json')['registry']; doc,ledger=build(registry)
 out=RUN/'authored'; out.mkdir(exist_ok=False)
 (out/'inventory.json').write_bytes(canonical_bytes(doc)+b'\n'); (out/'identity-registry.json').write_bytes(canonical_bytes(doc['registry'])+b'\n')
 write(f'{REL}/region-ledger-draft.json',ledger)
 write(f'{REL}/lineage.json',{'policy':'Retired placeholder identities retained in registry; new authored region UUIDs are independent. This source inventory split proposal conveys no semantic acceptance.','splits':[{'retired_placeholder':r,'new_region_ids':[l['region_id'] for l in ledger if l['page']==p]} for p,r in enumerate(read(f'{BASE}/inventory-one/inventory.json')['regions'][:4],1)]})
 write(f'{REL}/context-overread.json',{'initial_probe':pin(f'{REL}/context-access-authorization.json'),'observed':'Initial 55-point-high probe also exposed the first two lines and part of a counter for the next entry. This accidental neighboring content is retained in the initial probe, is not analyzed or incorporated, and contributes zero denominator.','correction':'Final context crop reduced to y=50..78 points, containing only the two-line Triarii completion.','impact':'Bounded context-access deviation disclosed for independent review; no page 5 substantive inventory.'})
 print('Authored',len(ledger),'regions plus 40 unchanged placeholders and 1 context region')
