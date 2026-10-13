"""Freeze synthetic cases; expectations are authored from the proposal, not validator output."""
import copy
import hashlib
import json
from pathlib import Path

SCHEMA = json.loads(Path('contracts/ig/source.schema.json').read_text())
OUT = Path('tests/contracts/fixtures')
OUT.mkdir(parents=True, exist_ok=True)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, ensure_ascii=False,
                                     separators=(',', ':')).encode()).hexdigest()


def seal(record):
    r=copy.deepcopy(record)
    if r['record_type']=='node':
        for aspect in r['data']['aspects']:
            aspect['aspect_hash']=digest({k:v for k,v in aspect.items() if k!='aspect_hash'})
    r['content_hash']=digest({k:v for k,v in r.items() if k not in ['content_hash','revision_id']})
    r['revision_id']='sha256:'+r['content_hash']
    return r


def record(key,kind,data):
    return seal({'id':'synthetic:'+key,'record_type':kind,'schema_version':'wgc-source-1',
                 'run_id':'synthetic:run','supersedes_refs':[], 'lineage_refs':[], 'data':data})


def active(r,aspect=None):
    ref={'mode':'active','id':r['id'],'record_type':r['record_type']}
    if aspect: ref['aspect_id']=aspect
    return ref


def historical(r,aspect=None):
    return {**active(r,aspect),'mode':'historical','revision_id':r['revision_id']}


def na(reason='Explicitly outside the scope of this fictional mechanism.'):
    return {'knowledge':'not_applicable','representation':'literal','value':None,
            'reason':reason,'gap_refs':[],'evidence_refs':[],'scope_refs':[]}


def known(text,evidence,opaque=False):
    value={'kind':'text','text':text} if not opaque else {
        'kind':'opaque','text':text,'execution_limitation':'No formal transition or cancellation policy is established.'}
    return {'knowledge':'known','representation':'literal','value':value,
            'reason':None,'gap_refs':[],'evidence_refs':[active(evidence)],'scope_refs':[]}


def unknown(gap,reason='The synthetic source does not specify the unit.'):
    return {'knowledge':'unknown','representation':'literal','value':None,
            'reason':reason,'gap_refs':[active(gap)],'evidence_refs':[],'scope_refs':[]}


def node(key,kind,description,aspects=None,groups=None):
    return record(key,'node',{'title':key,'editorial_parent_ref':None,
        'aspects':aspects or [],'semantic_groups':groups or [],'description':{'kind':kind,**description}})


def build_base():
    run=record('run','run',{'context_manifest_sha256':'0'*64,'raw_proposal_sha256':None,
      'model':None,'reasoning':None,'configuration_evidence':'Synthetic run: no actual model involved.',
      'started_utc':'2000-01-01T00:00:00Z','ended_utc':None,
      'measurements':{'wall_milliseconds':None,'input_tokens':None,'output_tokens':None,
                      'unknown_reason':'Synthetic fixture; no measurements.'},
      'expectation_basis':'The fixture catalogue specifies structural outcomes independently.'})
    source=record('source','source',{'role':'rulebook','publisher':'Imaginary publisher','system':'Copper tokens',
       'edition':'synthetic-1','language':'en','part':'entire fictional leaflet','media_type':'application/pdf',
       'byte_count':10,'sha256':hashlib.sha256(b'synthetic!').hexdigest(),'availability':'available',
       'compatibility':na('Only one fictional edition is asserted.'),'gap_refs':[]})
    regions=[]
    for page in [1,2]:
        regions.append(record('region'+str(page),'region',{'source_ref':historical(source),
          'pdf_page':page,'printed_label':str(page+5),'reading_order':0,
          'locator':{'kind':'box','coordinate_convention':'normalized-top-left',
                     'x0':0,'y0':0,'x1':500000,'y1':500000}}))
    evidence=record('evidence','evidence',{'region_refs':[historical(r) for r in regions],
      'role':'direct','literal_text':'If a copper token is lit, spend one spark. Resume after a reaction; cancellation is unspecified.',
      'normalized_text':None,'uncertain_symbols':[]})
    gap=record('gap','gap',{'kind':'unsupported_interpretation',
      'reason':'Cancellation and unit details are absent from the fictional excerpt.',
      'affected_refs':[],'blocked_operations':['formalization','execution'],'candidate_refs':[]})
    condition={'aspect_id':'lit-condition','aspect_hash':'0'*64,'facet':'condition',
      'statement':known('A copper token is lit.',evidence),'normative':True,
      'execution_impact':'formal','informational_review_ref':None}
    effect={'aspect_id':'spend-effect','aspect_hash':'0'*64,'facet':'effect',
      'statement':known('Spend one spark, then resume after a reaction.',evidence,True),'normative':True,
      'execution_impact':'blocking','informational_review_ref':None}
    clause=node('clause','clause',{'description':known('A single clause spans both pages.',evidence)},
      [condition,effect],[{'group_id':'lit-spend','operator':'all','conditions':['lit-condition'],
                          'effects':['spend-effect'],'exceptions':[],'timing':[]}])
    inventory=node('inventory','section',{'description':known('Two nonoverlapping fictional regions.',evidence)})
    retired=node('retired-concept','concept',{'description':known('A historical term, not an active rule.',evidence)})
    mechanical=[]
    for variant in SCHEMA['$defs']['node_description']['oneOf']:
        kind=variant['properties']['kind']['const']
        if kind in ['section','clause','concept','diagram','component','table']:continue
        fields={key:na() for key in variant['properties'] if key!='kind'}
        # Each mechanism has a source-backed, addressable descriptor. Others
        # explicitly retain their unknown/not-applicable state.
        first=next(iter(fields))
        fields[first]=known('Synthetic source descriptor for '+kind+'.',evidence)
        if kind=='parameter': fields['unit']=unknown(gap)
        if kind=='choice':
            fields['binding_id']=known('selected-copper-token',evidence)
            fields['lifetime']=known('This procedure invocation.',evidence)
            fields['reselection_policy']=known('Keep the participant until invocation completion.',evidence)
        if kind=='randomizer':
            fields['physical_symbols']=known('Two amber disks and one blue disk.',evidence)
            fields['pool_multiplicities_or_instances']=known('Amber has multiplicity two; blue has multiplicity one.',evidence)
            fields['replacement']=known('No replacement within a draw.',evidence)
        if kind=='state_variable':
            fields['value_type']=known('Nonnegative integer.',evidence)
            fields['unit']=known('sparks',evidence)
            fields['reset']=known('Reset at the opening of this token activation.',evidence)
        if kind=='event_type':
            fields['cause_filter']=known('This attempted token action, not a loss event.',evidence)
            fields['attempt_commit_invalidation']=known('An invalidated attempt does not commit its write.',evidence)
            fields['read_moment']=known('Read before paying the attempt cost.',evidence)
            fields['ordered_writes']=known('First pay sparks; then record the attempted action.',evidence)
        if kind=='continuation':
            fields['invocation_frame']=known('The particular invocation of the copper-token procedure.',evidence)
            fields['local_environment']=known('Retain the selected token binding.',evidence)
            fields['return_point']=known('Return to the step after the interrupted payment.',evidence)
        if kind=='cost':
            fields['amount']=known('One spark.',evidence)
            fields['amount']['value']={'kind':'quantity','amount':1,'unit':'sparks'}
            fields['attempt_or_success']=known('Pay on the first valid attempt.',evidence)
            fields['pay_once_key']=known('Invocation ID and copper payment step.',evidence)
        if kind=='calculation':
            fields['unit']=known('One half spark.',evidence)
            fields['unit']['value']={'kind':'rational','numerator':1,'denominator':2,'unit':'sparks'}
            fields['rounding_stage']=known('After multiplying the selected participants, before lookup.',evidence)
        if kind=='geometry':
            fields['map']=known('Fictional copper map.',evidence)
            fields['occupied_hexes']=known('One entity occupies cells C1 and C2.',evidence)
            fields['anchor']=known('C1 is the anchor.',evidence)
            fields['orientation']=known('Facing from C1 toward C2.',evidence)
        if kind=='visibility':
            for key in ['domains','rejected_choices','reason_codes','proof_paths','gaps','identifiers','cursor_metadata','caches']:
                fields[key]=known('Only player-visible information may appear in '+key+'.',evidence)
        if kind=='procedure': fields['termination']=unknown(gap,'No loop termination is specified.')
        mechanical.append(node(kind,kind,fields))
    table=node('table','table',{'axes':[{'axis_id':'heat','order':0,'unit':known('sparks',evidence),
      'boundaries':known('Zero through two, inclusive.',evidence)}],
      'cells':[{'cell_id':'low','axis_members':['heat'],
                'coordinates':[{'axis_id':'heat','position':known('Zero sparks.',evidence)}],
                'value':known('Dim',evidence),'merged_members':[]}],
      'notes':[{'note_id':'cap','cell_ids':['low'],'axis_ids':[],
                'statement':known('This note applies only to the low cell.',evidence)}],
      **{key:na() for key in ['out_of_range','missing_cell','decorations','legend','participant_bindings']}})
    profile=record('profile','profile',{'system':'Copper tokens','edition':'synthetic-1','rules_mode':'fictional',
      'options':[],'scenario':na(),'map_refs':[],'counter_refs':[],
      'material_refs':[historical(source)],'compatibility_decisions':[na()]})
    review=record('review','review',{'kind':'interpretation','actor':'Fictional fixture owner',
      'actor_role':'human_owner','authorization':'Synthetic owner role only; no real acceptance.',
      'decision':'accepted','decision_artifact':'synthetic:statement-of-lit-condition',
      'targets':[historical(clause,'lit-condition')], 'basis':[historical(source),historical(evidence)],
      'basis_completeness':'complete','scope':'Only the lit-condition aspect; not the effect.',
      'rationale':'Synthetic scoped decision used to test metadata and freshness.', 'supersedes_review_refs':[]})
    cover=[]
    for index,r in enumerate(regions):
        cover.append(record('coverage'+str(index),'coverage',{'inventory_ref':historical(inventory),
          'region_ref':historical(r),'level':'transcription','status':'represented',
          'target_refs':[active(clause)],'gap_refs':[],'denominator_role':'inventory',
          'exclusion_reason':None,'scope_decision_ref':None}))
    binding=record('binding','origin_binding',{'input_snapshot_id':'synthetic:input','input_sha256':'1'*64,
      'relative_path':'kb/clauses.json','field_locator':'/clauses/by-key/copper',
      'ig_refs':[active(clause)],'external_namespace':'kb-fictional','external_id':'copper', 'mapping_status':'partial'})
    registry=record('identities','identity_registry',{'entries':[{'origin_key':'fictional-term-copper',
      'id':clause['id'],'status':'assigned','candidate_ids':[],'gap_refs':[]}]})
    historical_relation=record('history-link','relation',{'relation_type':'mention','from_ref':active(clause),
      'target_status':'resolved','target_ref':historical(retired),'raw_locator':None,'edition':'synthetic-1',
      'candidate_refs':[],'gap_refs':[],'applicability':na(),'evidence_refs':[active(evidence)],
      'requirement':'informational','requirement_group':{'group_id':'navigation','operator':'all'}})
    records=[run,source,*regions,evidence,gap,clause,inventory,retired,*mechanical,table,
             profile,review,*cover,binding,registry,historical_relation]
    selected=[r for r in records if r['id']!=retired['id']]
    snapshot=record('snapshot','snapshot',{'state':'sealed','selected':[
      {k:r[k] for k in ['id','record_type','revision_id','content_hash']} for r in selected],
      'profile_ref':active(profile),'conflict_refs':[],
      'assessments':{'import':{'status':'complete','basis_refs':[historical(binding)]},
        'coverage_refs':[active(c) for c in cover],'semantic_review_refs':[active(review)],
        'executable':{'status':'blocked','scope_refs':[active(clause)],'blocker_refs':[active(gap)],
          'reason':'Opaque effect and incomplete formal semantics; source validation grants no execution.'}}})
    return {'schema_version':'wgc-source-1','snapshot_id':snapshot['id'],'records':records+[snapshot]}


def get(bundle,key):
    return next(r for r in bundle['records'] if r['id']=='synthetic:'+key)


def replace(bundle,key,mutate,preserve=False):
    old=get(bundle,key); new=copy.deepcopy(old); mutate(new); new=seal(new)
    if preserve: bundle['records'].append(new)
    else: bundle['records'][bundle['records'].index(old)]=new
    snapshot=get(bundle,'snapshot')
    for entry in snapshot['data']['selected']:
        if entry['id']==old['id']:
            entry.update({k:new[k] for k in ['id','record_type','revision_id','content_hash']})
    bundle['records'][bundle['records'].index(snapshot)]=seal(snapshot)
    return new


catalog=[]
def save(name,bundle,valid,expectation,basis,report=None,error=None):
    filename=name+'.json'
    (OUT/filename).write_text(json.dumps(bundle,indent=2)+'\n',encoding='utf-8')
    catalog.append({'file':filename,'valid':valid,'expectation':expectation,
                    'basis':basis,'report':report or {},'error_contains':error})


base=build_base()
save('valid-source',base,True,'All source mechanisms are addressable; import complete and two represented transcription regions do not permit execution.',
 'IG-1A criteria 1, 3, 4; IG-DATA-MODEL: Collections, Reviews and readiness; IG-MECHANICS-PROFILES.',
 {'execution':'blocked','review_freshness':'current','transcription_represented':2})
save('valid-historical-reference',base,True,'The retired concept is in the store but is not selected. A historical mention may resolve it.',
 'IG-DATA-MODEL: Identity and record envelope, historical versus active resolution.',{'execution':'blocked'})
b=copy.deepcopy(base)
replace(b,'review',lambda r:r['data'].update(basis_completeness='partial'))
save('valid-partial-review',b,True,'Incomplete review basis cannot establish current freshness.',
 'IG-DATA-MODEL: Reviews and readiness, incomplete basis implies unknown.',{'review_freshness':'unknown'})
b=copy.deepcopy(base)
old=copy.deepcopy(get(b,'clause'))
def change_aspect(r):
    r['supersedes_refs']=[historical(old)]
    r['data']['aspects'][0]['statement']['value']['text']='A copper token is warm.'
replace(b,'clause',change_aspect,preserve=True)
save('valid-changed-aspect',b,True,'Same stable aspect ID, changed meaning and revision: old scoped acceptance is stale.',
 'IG-WGU-ARCHITECTURE: Acceptance is never inherited by a changed aspect.',{'review_freshness':'stale'})
b=copy.deepcopy(base)
old=copy.deepcopy(get(b,'source'))
replace(b,'source',lambda r:r['data'].update(edition='synthetic-2'),preserve=True)
save('valid-changed-dependency',b,True,'An exact source basis is no longer selected; review becomes stale even with unchanged target.',
 'IG-WGU-ARCHITECTURE: Review bases pin evidence, profile and dependencies.',{'review_freshness':'stale'})
b=copy.deepcopy(base)
def unknown_no_gap(r):r['data']['description']['unit']['gap_refs']=[]
replace(b,'parameter',unknown_no_gap)
save('invalid-unknown-without-gap',b,False,'Unknown unit needs a null value, reason and a gap.',
 'IG-DATA-MODEL: Knowledge and representation.',error='schema')
b=copy.deepcopy(base)
get(b,'clause')['data']['aspects'][0]['statement']['value']['text']='Unhashed changed condition.'
r=get(b,'clause');r['content_hash']=digest({k:v for k,v in r.items() if k not in ['content_hash','revision_id']});r['revision_id']='sha256:'+r['content_hash']
save('invalid-changed-aspect-hash',b,False,'Container hash cannot conceal a stale aspect hash.',
 'IG-1A ID and revision hash criterion; stable aspect content integrity.',error='changed aspect hash')
b=copy.deepcopy(base)
replace(b,'review',lambda r:r['data'].update(actor_role='model'))
save('invalid-model-approval',b,False,'A model may observe but cannot grant semantic acceptance.',
 'IG-DATA-MODEL: Only an authorized human grants semantic acceptance.',error='schema')
b=copy.deepcopy(base)
replace(b,'history-link',lambda r:r['data'].update(target_ref=active(get(b,'retired-concept'))))
save('invalid-dangling-active',b,False,'A stored historical revision does not activate its identity.',
 'IG-DATA-MODEL: References used as active rules resolve only in the selected snapshot.',error='dangling active')
b=copy.deepcopy(base)
b['records'].remove(get(b,'retired-concept'))
save('invalid-dangling-historical',b,False,'Exact historical references must resolve in the supplied immutable store.',
 'IG-DATA-MODEL: Historical review and supersession references resolve in immutable revision store.',error='dangling historical')
b=copy.deepcopy(base)
s=get(b,'snapshot');s['data']['selected'].append(copy.deepcopy(s['data']['selected'][0]));b['records'][-1]=seal(s)
save('invalid-duplicate-selection',b,False,'Only one revision per identity may be selected.',
 'IG-DATA-MODEL: A snapshot selects at most one revision per ID.',error='duplicate identity')
b=copy.deepcopy(base);b['records'].append(copy.deepcopy(get(b,'clause')))
save('invalid-duplicate-store',b,False,'The revision store cannot contain a duplicate identity/revision.',
 'IG-DATA-MODEL: Validate identity/revision uniqueness.',error='duplicate identity')
b=copy.deepcopy(base)
replace(b,'clause',lambda r:r['data']['aspects'][1].update(execution_impact='formal'),preserve=True)
save('invalid-opaque-formal',b,False,'A normative opaque effect cannot be labelled formal.',
 'IG-LEGAL-ACTIONS: Opaque meaning affecting effect blocks executable readiness.',error='opaque normative')
b=copy.deepcopy(base)
get(b,'snapshot')['data']['assessments']['executable']['status']='ready';b['records'][-1]=seal(get(b,'snapshot'))
save('invalid-opaque-ready',b,False,'The source contract cannot claim executable readiness, including when import is complete.',
 'IG-1A: Source-level opaque is accepted without granting execution.',error='schema')
b=copy.deepcopy(base)
replace(b,'clause',lambda r:r['data']['semantic_groups'][0].update(conditions=['spend-effect']),preserve=True)
save('invalid-group-binding',b,False,'Condition/effect composition must select the correctly typed stable aspects.',
 'IG-DATA-MODEL: Shared subject ID does not bind conditions to effects.',error='semantic group member')
b=copy.deepcopy(base)
replace(b,'table',lambda r:r['data']['description']['notes'][0].update(cell_ids=['missing-cell']))
save('invalid-table-note',b,False,'A note must address an existing axis or cell.',
 'IG-DATA-MODEL: Validate table notes/axes; IG-MECHANICS-PROFILES: note scopes.',error='table note scope')
b=copy.deepcopy(base)
replace(b,'parameter',lambda r:r['data']['description']['value_type'].update(evidence_refs=[]))
save('invalid-known-without-evidence',b,False,'Known is an evidenced proposal; an empty evidence list does not establish it.',
 'IG-DATA-MODEL: Knowledge states.',error='schema')
b=copy.deepcopy(base)
replace(b,'history-link',lambda r:r['data'].update(target_ref={**historical(get(b,'retired-concept')),'record_type':'source'}))
save('invalid-reference-type',b,False,'A concept cannot resolve as a source record.',
 'IG-DATA-MODEL: Validate typed references.',error='typed reference mismatch')
b=copy.deepcopy(base)
replace(b,'binding',lambda r:r['data'].update(relative_path='../neighbour/clauses.json'),preserve=True)
save('invalid-origin-path',b,False,'Origin locators are relative safe paths, never traversal.',
 'IG-WGU-ARCHITECTURE: safe paths and path escapes.',error='safe relative')
b=copy.deepcopy(base)
replace(b,'identities',lambda r:r['data']['entries'].append(copy.deepcopy(r['data']['entries'][0])))
save('invalid-anonymous-identity-conflict',b,False,'One persisted origin key cannot silently rematch to multiple identities.',
 'IG-DATA-MODEL: anonymous identities use persisted registry; ambiguous rematches are conflicts.',error='registry origin key')
b=copy.deepcopy(base)
replace(b,'coverage0',lambda r:r['data'].update(gap_refs=[active(get(b,'gap'))]))
save('invalid-gap-counted-as-coverage',b,False,'A gap cannot count as represented content.',
 'IG-WGU-ARCHITECTURE: Gaps never count as represented content.',error='represented coverage')
# A procedure graph cycle is structurally legal; it grants no execution and its
# missing termination remains an explicit gap.
b=copy.deepcopy(base)
procedure=get(b,'procedure');step=get(b,'step')
for key,frm,to in [('cycle-a',procedure,step),('cycle-b',step,procedure)]:
    link=record(key,'relation',{'relation_type':'procedure_use','from_ref':active(frm),
       'target_status':'resolved','target_ref':active(to),'raw_locator':None,'edition':'synthetic-1',
       'candidate_refs':[],'gap_refs':[],'applicability':known('Invocation uses this step.',get(b,'evidence')),
       'evidence_refs':[active(get(b,'evidence'))],'requirement':'required',
       'requirement_group':{'group_id':'cycle','operator':'all'}})
    b['records'].insert(-1,link)
    get(b,'snapshot')['data']['selected'].append({k:link[k] for k in ['id','record_type','revision_id','content_hash']})
b['records'][-1]=seal(get(b,'snapshot'))
save('valid-procedure-cycle',b,True,'Source graphs may be cyclic. Missing termination blocks formalization/execution, not source storage.',
 'IG-DATA-MODEL: rule graphs may contain cycles; procedures need termination rules.',{'execution':'blocked'})
b=copy.deepcopy(base)
replace(b,'profile',lambda r:r['data'].update(compatibility_decisions=[unknown(get(b,'gap'),'Two fictional editions conflict; no precedence is established.')]))
save('valid-edition-conflict',b,True,'An unresolved compatibility decision is preserved as unknown, never newer-wins.',
 'IG-WGU-ARCHITECTURE: exact editions and no universal precedence.',{'execution':'blocked'})
b=copy.deepcopy(base)
base_chapter=node('chapter-a','section',{'description':known('Base rule section.',get(b,'evidence'))})
exception_chapter=node('chapter-b','section',{'description':known('A separate exception section.',get(b,'evidence'))})
replace(b,'clause',lambda r:r['data'].update(editorial_parent_ref=active(base_chapter)),preserve=True)
exception=node('exception-clause','clause',{'description':known('An unlit token cannot invoke payment.',get(b,'evidence'))})
exception['data']['editorial_parent_ref']=active(exception_chapter);exception=seal(exception)
link=record('cross-section-exception','relation',{'relation_type':'exception',
 'from_ref':active(exception),'target_status':'resolved','target_ref':active(get(b,'clause')),
 'raw_locator':None,'edition':'synthetic-1','candidate_refs':[],'gap_refs':[],
 'applicability':known('Only an unlit token.',get(b,'evidence')),'evidence_refs':[active(get(b,'evidence'))],
 'requirement':'conditional','requirement_group':{'group_id':'separate-exception','operator':'all'}})
for r in [base_chapter,exception_chapter,exception,link]:
 b['records'].append(r)
 get(b,'snapshot')['data']['selected'].append({k:r[k] for k in ['id','record_type','revision_id','content_hash']})
s=get(b,'snapshot');b['records'][b['records'].index(s)]=seal(s)
save('valid-cross-section-exception',b,True,'Exception points from modifying clause in a separate section to the base clause; editorial parent is not a dependency.',
 'IG-DATA-MODEL: Exception/modification direction and cross-chapter tests.',{'execution':'blocked','review_freshness':'current'})
b=copy.deepcopy(base)
overlap=copy.deepcopy(get(b,'region1'));overlap['id']='synthetic:overlapping-region'
overlap['data']['locator'].update(x0=100000,x1=400000);overlap=seal(overlap)
cover=copy.deepcopy(get(b,'coverage0'));cover['id']='synthetic:overlapping-coverage'
cover['data']['region_ref']=historical(overlap);cover=seal(cover)
for r in [overlap,cover]:
 b['records'].insert(-1,r)
 get(b,'snapshot')['data']['selected'].append({k:r[k] for k in ['id','record_type','revision_id','content_hash']})
b['records'][-1]=seal(get(b,'snapshot'))
save('invalid-overlapping-coverage',b,False,'Overlapping inventory regions cannot both enter the transcription denominator.',
 'IG-DATA-MODEL: Validate coverage denominators; no overlapping context in denominator.',error='overlapping coverage')
b=copy.deepcopy(base)
context=copy.deepcopy(get(b,'coverage0'));context['id']='synthetic:context-coverage'
context['data']['denominator_role']='context';context=seal(context)
b['records'].insert(-1,context)
get(b,'snapshot')['data']['selected'].append({k:context[k] for k in ['id','record_type','revision_id','content_hash']})
b['records'][-1]=seal(get(b,'snapshot'))
save('valid-overlapping-context',b,True,'A context-only entry does not add the same region to the denominator.',
 'IG-DATA-MODEL: Do not add overlapping context regions to denominator.',{'transcription_represented':2})
(OUT/'catalog.json').write_text(json.dumps({'format':'wgc-synthetic-oracles-1','cases':catalog},indent=2)+'\n',encoding='utf-8')
print('Frozen',len(catalog),'independently specified cases.')
