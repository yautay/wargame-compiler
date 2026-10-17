import json
from pathlib import Path

def obj(properties):
    return {'type':'object','properties':properties,'required':list(properties),'additionalProperties':False}
def array(items, minimum=0): return {'type':'array','items':items,'minItems':minimum}
def ref(name): return {'$ref':'#/$defs/'+name}
def nullable(shape): return {'oneOf':[{'type':'null'},shape]}
text={'type':'string','minLength':1}
integer={'type':'integer'}
positive={'type':'integer','minimum':1}
nonnegative={'type':'integer','minimum':0}
hash_={'type':'string','pattern':'^[0-9a-f]{64}$'}
box=array({'type':'integer','minimum':0,'maximum':1000000},4)
native_box=array(integer,4)
pin=obj({'path':text,'bytes':nonnegative,'sha256':hash_})
coverage=obj({'status':{'enum':['represented','partial','unprocessed','excluded']},'reason':nullable(text),'gap':{'type':'boolean'},'boundary':nullable(ref('boundary'))})
defs={
 'pin':pin,
 'box':box,
 'registry':obj({'format':{'const':'wgc-source-identities-1'},'source_id':text,'source_revision':hash_,'entries':array(obj({'kind':{'enum':['page','region']},'key':text,'id':text}))}),
 'boundary':obj({'source_revision':hash_,'partition_hash':hash_,'region_id':text,'box':box,'level':{'enum':['transcription','descriptive_semantics','formal_semantics']},'actor':text,'actor_role':{'enum':['human_owner','human_reviewer']},'authorization':text,'rationale':text,'decision':pin}),
 'page':obj({'id':text,'key':text,'revision':hash_,'source_revision':hash_,'pdf_page':positive,'label':obj({'status':{'enum':['unknown','embedded_unverified','verified']},'value':nullable(text),'reason':nullable(text),'evidence':nullable(text)}),'media_box':native_box,'crop_box':native_box,'effective_crop_box':native_box,'rotation':{'enum':[0,90,180,270]},'user_unit':obj({'numerator':positive,'denominator':positive})}),
 'region':obj({'id':text,'key':text,'revision':hash_,'source_revision':hash_,'page_id':text,'box':box,'kind':{'enum':['unclassified','heading','clause','table','note','example','diagram','legend','editorial']},'denominator_role':{'enum':['inventory','context']},'uncertainty':array(text),'coverage':obj({level:coverage for level in ['transcription','descriptive_semantics','formal_semantics']})}),
 'evidence':obj({'id':text,'source_sha256':hash_,'region_id':text,'region_revision':hash_,'page_id':text,'pdf_page':positive,'box':box,'crop_pdf':pin,'text':pin,'image':pin,'text_codepoints':nonnegative,'text_offsets':obj({'unit':{'const':'unicode_codepoints'},'bounds':{'const':'half_open'},'start':nonnegative,'end':nonnegative}),'text_parameters':obj({'engine':{'const':'pdfplumber'},'version':text,'x_tolerance':nonnegative,'y_tolerance':nonnegative,'layout':{'const':False}}),'render_parameters':obj({'engine':{'const':'poppler-pdftoppm'},'version':text,'dpi':{'type':'integer','minimum':36,'maximum':600},'cropbox':{'const':True},'format':{'const':'png'},'width_pixels':positive,'height_pixels':positive}),'crop_parameters':obj({'engine':{'const':'pypdf'},'version':text,'user_unit_normalized':{'const':True},'frame':{'const':'displayed-crop-top-left'}}),'uncertainty':array(text,1)})
}
schema=obj({'format':{'const':'wgc-inventory-1'},'revision':hash_,'source':obj({'id':text,'sha256':hash_,'pdf':pin,'provenance':pin,'page_count':positive,'independent_counts':array(obj({'tool':text,'count':positive}),2)}),'pages':array(ref('page'),1),'regions':array(ref('region')),'registry':ref('registry'),'reading_order':array(text),'links':array(obj({'kind':{'enum':['continuation','note_for','illustrates']},'from':text,'to':text,'reason':text})),'evidence':array(ref('evidence')),'toolchain':array(obj({'name':text,'version':text}))})
schema.update({'$schema':'https://json-schema.org/draft/2020-12/schema','$id':'urn:wgc:inventory:1','title':'WGC independent page and region inventory','description':'Integer-only geometry and exact artifact pins. Cross-record, hash, overlap, identity, exclusion freshness and page-completeness checks require wgc.sources.inventory.validate. No semantic acceptance.','$defs':defs})
p=Path(__file__).parent/'product/contracts/ig/regions.schema.json'; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(json.dumps(schema,indent=2)+'\n',encoding='utf-8')
