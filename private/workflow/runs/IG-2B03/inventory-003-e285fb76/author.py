"""Bounded, reproducible authoring for IG-2B03 only. No old output is mutated."""
import copy, json, pathlib, math, hashlib
from wgc.sources.inventory import make_region, seal, validate, file_pin
from wgc.contracts.source import canonical_bytes

ROOT=pathlib.Path.cwd()
OUT=pathlib.Path(__file__).parent
PREP=pathlib.Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76')
PINS=json.loads((PREP/'input-pins.json').read_text())
BASE=json.loads(pathlib.Path(PINS['files'][0]['path']).read_text())
META={k:v for k,v in json.loads((OUT/'claim.json').read_text()).items() if k in ('role','actor','task','model','reasoning','configuration_evidence','configuration_sha256')}

# Explicit keys are authored identities; line ranges supply coordinates, not identity.
# A range is inclusive and uses the separately frozen machine line ledger for that page.
PLAN={
9:[
 ('434','clause',2,4),('435','clause',5,10),('43-design-note','note',11,17),
 ('44-heading','heading',18,18),('44-introduction','clause',19,22),
 ('44-item-1','clause',23,24),('44-item-2','clause',25,27),('44-item-3','clause',28,28),
 ('44-item-4','clause',29,29),('44-item-5','clause',30,31),('44-item-6','clause',32,33),
 ('44-historical-note','note',34,44),('45-heading','heading',46,47),('45-introduction','clause',48,54),
 ('451','clause',55,61),('452','clause',62,71),('452-exception','note',72,74),
 ('453','clause',75,80),('453-play-note','note',81,84),('454','clause',85,92),
 ('455','clause',93,95),('456-start','clause',96,98)],
10:[
 ('456-continuation','clause',1,2),('456-bullet-1','clause',3,4),('456-bullet-2','clause',5,7),
 ('46-heading','heading',8,8),('46-body','clause',9,17),('46-exception','note',18,19),
 ('46-historical-digression','note',20,28),('47-heading','heading',29,29),
 ('471','clause',30,35),('472','clause',36,51),('473','clause',53,60),('474','clause',61,71),
 ('474-design-note','note',72,75),('475','clause',76,77),('48-heading','heading',78,78),
 ('48-introduction','clause',79,80),('481','clause',81,83),('482','clause',84,87),
 ('483','clause',88,96),('484','clause',97,99),('484-design-note','note',100,102)],
11:[
 ('485','clause',2,5),('49-heading','heading',6,6),('491-introduction','clause',7,10),
 ('491-bullet-1','clause',11,14),('491-bullet-2','clause',15,19),('492-introduction','clause',20,23),
 ('492-bullet-1','clause',24,25),('492-bullet-2','clause',26,27),('492-bullet-3','clause',28,29),
 ('492-closing','clause',30,30),('493','clause',31,33),('494','clause',34,36),
 ('50-heading','heading',37,38),('50-introduction','clause',39,44),('50-important','note',45,47),
 ('51-heading','heading',48,48),('511-start','clause',49,50),('511-continuation','clause',52,53),
 ('512','clause',54,61),('513','clause',62,63),('513-exceptions','note',64,65),
 ('513-activation-example','example',66,72),('514','clause',73,75),('514-exceptions','note',76,77),
 ('515-introduction','clause',78,78),('515-bullet-1','clause',79,80),('515-bullet-2','clause',81,81),
 ('515-bullet-3','clause',82,82),('515-bullet-4','clause',83,84),('515-bullet-5','clause',85,85),
 ('515-bullet-6','clause',86,86),('515-closing','clause',87,89),('515-exception','note',90,90),
 ('52-heading','heading',91,91),('521','clause',92,94),('521-example','example',95,98),
 ('522-introduction','clause',99,100)],
12:[
 ('522-item-1','clause',1,2),('522-item-2','clause',3,4),('522-item-3','clause',5,5),
 ('522-item-4','clause',6,6),('522-item-5','clause',7,7),('522-item-6','clause',8,9),
 ('522-item-7','clause',10,11),('522-closing','clause',12,16),('523-introduction','clause',17,18),
 ('523-item-1','clause',19,21),('523-item-2','clause',22,23),('523-closing','clause',24,24),
 ('524','clause',25,28),('524-example','example',29,34),('525','clause',35,38),
 ('526-paragraph-1','clause',39,46),('526-paragraph-2-start','clause',47,52),
 ('526-paragraph-2-continuation','clause',54,54),('526-example','example',55,59),
 ('527','clause',60,62),('528-introduction','clause',63,64),('528-item-1','clause',65,66),
 ('528-item-2','clause',67,67),('528-closing','clause',68,69),('53-heading','heading',70,70),
 ('53-play-note','note',71,75),('531-introduction','clause',76,80),('531-bullet-1','clause',81,82),
 ('531-bullet-2','clause',83,83),('531-bullet-3','clause',84,84),('532','clause',85,88),
 ('532-example','example',89,90),('533-introduction','clause',91,92),('533-bullet-0-1','clause',93,97),
 ('533-bullet-2-8','clause',98,98),('533-bullet-9','clause',99,100),('534','clause',101,103)]}

def box(points):
 x0,y0,x1,y1=points
 return [math.floor(x0/612*1000000),math.floor(y0/792*1000000),math.ceil(x1/612*1000000),math.ceil(y1/792*1000000)]

def specs():
 rows=[]
 for n,plan in PLAN.items():
  lines=json.loads((OUT/f'lines-{n}.json').read_text(encoding='utf-8'))
  def add(slug,kind,bounds,idx=None,observation=None):
   rows.append({'page':n,'slug':slug,'key':f'spqr5e:p{n:02d}:{slug}', 'kind':kind,'box':box(bounds),
                'pdf_points_top_left':[str(v) for v in bounds],'line_indices':idx or [],'observation':observation})
  add('running-title','editorial',(207,26.5,405,38),observation='Running title and edition; retained in denominator, not excluded.')
  add('printed-label','editorial',((556.5 if n%2 else 44.5),24,(568 if n%2 else 56),37),observation=f'Visible printed label {n}; physical and printed addresses separately pinned.')
  add('header-rule','editorial',(44.5,39.5,567.5,40.8),observation='Horizontal running-header separator; graphic editorial region.')
  for slug,kind,start,end in plan:
   ls=lines[start:end+1];assert len({l['column'] for l in ls})==1
   col=ls[0]['column'];x0,x1=(44.4,297.7) if col=='L' else (314.4,567.7)
   if slug in ('44-introduction','491-introduction'):x0=89.6
   top=min(l['top'] for l in ls)-0.8;bottom=max(l['bottom'] for l in ls)+0.8
   if slug in ('43-design-note','44-historical-note','453-play-note','46-historical-digression','474-design-note','484-design-note','53-play-note'):top-=2.7;bottom+=2.7
   if slug=='50-important':x0=44.4;x1=297.7;top=647.7;bottom=690.5
   if slug=='44-introduction':
    add('44-commander-counter','diagram',(44.8,285.7,81.9,322.7),observation='T. Varro counter: all components separately located in component ledger; picture does not approve ratings or legality.')
   if slug=='491-introduction':
    add('49-elephant-counter','diagram',(44.8,128.3,81.9,165.2),observation='Elephant 1 counter: all components separately located in component ledger; glyphs are observations, not semantic approval.')
   add(slug,kind,(x0,top,x1,bottom),list(range(start,end+1)))
  add('copyright','editorial',(261,748.5,351,760),observation='Copyright furniture, retained as unprocessed inventory; no exclusion authorization.')
 return rows

def build(registry):
 doc=copy.deepcopy(BASE);doc['registry']=copy.deepcopy(registry)
 retired={r['id'] for r in PINS['replace_only_placeholders']}
 assert not any(e['region_id'] in retired for e in doc['evidence'])
 assert not any(l['from'] in retired or l['to'] in retired for l in doc['links'])
 doc['regions']=[r for r in doc['regions'] if r['id'] not in retired]
 rows=specs();new=[]
 for row in rows:
  page=next(p for p in doc['pages'] if p['pdf_page']==row['page'])
  reg=make_region(doc['registry'],row['key'],page,row['box'],kind=row['kind'],reason='Source independently inventoried; extracted bytes and visual observation are not a verified transcription or semantic representation.')
  reg['uncertainty']=['Independent source accounting only; transcription completeness and descriptive/formal semantics remain unprocessed.']
  reg=seal(reg);new.append(reg);row['region_id']=reg['id']
 by={(r['page'],r['slug']):r['region_id'] for r in rows}
 doc['regions'].extend(new)
 order=[]
 for ident in doc['reading_order']:
  if ident in retired:
   n=next(p['pdf_page'] for p in doc['pages'] if p['id']==next(r['page_id'] for r in BASE['regions'] if r['id']==ident))
   order.extend(row['region_id'] for row in rows if row['page']==n)
  else:order.append(ident)
 doc['reading_order']=order
 continuations=[(9,'456-start',10,'456-continuation','Literal sentence continues: "the other two" / "consuls were elsewhere."'),
  (11,'511-start',11,'511-continuation','Literal column continuation: "they" / "are then Finished."'),
  (11,'522-introduction',12,'522-item-1','List introduction continues onto next page with numbered items 1-7.'),
  (12,'526-paragraph-2-start',12,'526-paragraph-2-continuation','Literal column continuation: "all other leaders" / "are either Finished or in an enemy ZOC."')]
 for a,b,c,d,reason in continuations:doc['links'].append({'kind':'continuation','from':by[a,b],'to':by[c,d],'reason':reason})
 # Attach annotations without resolving the referenced gameplay meaning.
 notes=[(9,'43-design-note','435'),(9,'44-historical-note','44-introduction'),(9,'452-exception','452'),(9,'453-play-note','453'),
  (10,'46-exception','46-body'),(10,'46-historical-digression','46-body'),(10,'474-design-note','474'),(10,'484-design-note','484'),
  (11,'50-important','50-introduction'),(11,'513-exceptions','513'),(11,'514-exceptions','514'),(11,'515-exception','515-closing'),
  (12,'53-play-note','53-heading')]
 for n,a,b in notes:doc['links'].append({'kind':'note_for','from':by[n,a],'to':by[n,b],'reason':'Visible note/exception associated with adjacent text; structural link only.'})
 for n,a,b in [(9,'44-commander-counter','44-introduction'),(11,'49-elephant-counter','491-introduction'),(11,'513-activation-example','513'),(11,'521-example','521'),(12,'524-example','524'),(12,'526-example','526-paragraph-1'),(12,'532-example','532')]:doc['links'].append({'kind':'illustrates','from':by[n,a],'to':by[n,b],'reason':'Visible counter or source-labelled example; no semantic acceptance inferred.'})
 doc=seal(doc);validate(doc)
 return doc,rows

if __name__=='__main__':
 dest=OUT/'authored';dest.mkdir(exist_ok=False)
 doc,rows=build(BASE['registry'])
 for name,value in [('inventory.json',doc),('identity-registry.json',doc['registry']),('partition-plan.json',dict(META,regions=rows,reading_order_policy='Running furniture, left column top-to-bottom including counter adjacent to introduction, right column top-to-bottom, copyright. Explicit list controls reading order; extraction order is not authority.'))]:
  (dest/name).write_bytes(canonical_bytes(value)+b'\n')
 print(json.dumps({'regions':len(rows),'by_page':{str(n):sum(r['page']==n for r in rows) for n in PLAN},'full_regions':len(doc['regions'])}))
