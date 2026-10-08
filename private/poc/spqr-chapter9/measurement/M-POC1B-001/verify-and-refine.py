"""Local one-session artifact audit/refinement; no model invocation or rule execution."""
from pathlib import Path
import json, hashlib, copy, re
from collections import Counter
from datetime import datetime, timezone
import pdfplumber

ROOT=Path('C:/dev/wargame-compiler')
P=ROOT/'private/poc/spqr-chapter9'
S=P/'measurement/M-POC1B-001'
D=P/'evaluation/draft'
def read(p): return json.loads(p.read_text(encoding='utf-8-sig'))
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write_new(p,v):
    assert not p.exists(), p
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def replace_authored(p,v):
    p.write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')

docs={n:read(D/(n+'.json')) for n in ('expectations','dependencies','situations')}
prior=S/'initial-authored'
assert not prior.exists()
prior.mkdir()
for n in docs:
    (prior/(n+'.json')).write_bytes((D/(n+'.json')).read_bytes())

inv=read(D/'inventory.json')
items={r['id']:r for r in inv['items']}
for name in read(P/'evaluation/owner-review-001/review-manifest.json')['supplement_order']:
    for row in read(P/'evaluation/owner-review-001'/name).get('items',[]): items[row['id']]=row
deps=docs['dependencies']['dependencies']
for n,origin,target,kind,refs,reason in [
 (2,'TR-03','C-9.14-11','exception',['TR-03','C-9.14-11'],
  'Późniejszy7–9 Leader Elephant ma instead/immediately rallied, szczególny skutek wobec ogólnego no rally Rampage. Kierunek szczególnego wiersza→ogólny zakaz; zakres pierwszego rzutu osobno unresolved.'),
 (3,'C-9.86-01','C-9.14-11','condition',['C-9.86-01','C-9.14-11'],
  'Dopuszczenie szczególnej Scorpio reaction nie uchyla no Reaction Fire of any kind dla Rampaging EL. Ocena dostępności ognia potrzebuje tego ograniczenia celu; kierunek procedury ognia→warunek targeta, brak jawnego odsyłacza numerycznego.')]:
    ev=[]
    for ref in refs:
        for raw in items[ref]['evidence']:
            e=copy.deepcopy(raw)
            e.pop('human_review',None)
            e['inventory_ref']=ref
            e['M_POC1B_read']='manual Codex source review; owner meaning review pending'
            ev.append(e)
    deps.append({'id':f'DEP-NEW-{n:03d}','candidate_ids':[],'from':origin,'to':target,
       'kind':kind,'explicitness':'implicit','executable':True,'target_status':'internal',
       'status':'source_supported_proposal','direction_reason':reason,'evidence':ev,
       'criticality':'critical','criticality_reason':'Błędne pierwszeństwo/zakres wyjątku zmienia rally lub legalność dodatkowego ognia.',
       'missing_target_effect':'Internal chapter source available; proposed conflict reading requires actual owner review.',
       'human_review_status':'waiting_review','owner_confirmed':False})
docs['dependencies']['new_relation_policy']='DEP-NEW-001/002/003 separately marked implicit internal proposals, no silent expansion of historical96.'
docs['dependencies']['new_proposals']=[r['id'] for r in deps if not r['candidate_ids']]
for exp in docs['expectations']['expectations']:
    for dep in deps[-2:]:
        if dep['from'] in exp['inventory_refs']:
            exp['dependency_ids'].append(dep['id'])
for sit in docs['situations']['situations']:
    for dep in deps[-2:]:
        if dep['from'] in sit['inventory_refs']:
            sit['dependency_ids'].append(dep['id'])

# Populate explicit dependency→expectation/situation traceability and vice versa.
for dep in deps:
    dep['expectation_ids']=[e['id'] for e in docs['expectations']['expectations'] if dep['id'] in e['dependency_ids']]
    dep['situation_ids']=[s['id'] for s in docs['situations']['situations'] if dep['id'] in s['dependency_ids']]
    dep['necessity_scope']='Full real-state execution' if dep['executable'] else ('Physical source completeness' if dep['kind']=='continuation' else 'Informational mention only')
    dep['relation_basis_status']='hypothesis_requires_target_evidence' if dep['id']=='DEP-031' else 'source_grounded_classification_proposal'

depdoc=docs['dependencies']
depdoc['counts']={'total':len(deps),'by_status':dict(Counter(r['status'] for r in deps)),
 'owner_confirmed':0,'owner_unconfirmed':len(deps),'by_criticality':dict(Counter(r['criticality'] for r in deps))}
for status in ('source_supported_proposal','requires_context','unresolved_interpretation'):
    depdoc['sets'][status]=[r['id'] for r in deps if r['status']==status]
den=depdoc['denominators']
den['execution_proposals_by_explicitness']=dict(Counter(r['explicitness'] for r in deps if r['executable']))
den['all_proposals_by_explicitness']=dict(Counter(r['explicitness'] for r in deps))
den['source_supported_execution_by_explicitness']=dict(Counter(r['explicitness'] for r in deps if r['executable'] and r['status']=='source_supported_proposal'))
den['unconfirmed_execution_by_explicitness']=dict(Counter(r['explicitness'] for r in deps if r['executable'] and not r['owner_confirmed']))
den['context_required_execution_by_explicitness']=dict(Counter(r['explicitness'] for r in deps if r['executable'] and r['status']=='requires_context'))
den['unresolved_interpretation_execution_by_explicitness']=dict(Counter(r['explicitness'] for r in deps if r['executable'] and r['status']=='unresolved_interpretation'))
depdoc['identity_and_review_limits']='No claim that127 proposal facets are127 distinct validated semantic edges. Repeated/alias targets need identity review; physical continuations and7 mentions excluded from execution counts. A target hypothesis is not proven by source wording alone.'

for n,doc in docs.items(): replace_authored(D/(n+'.json'),doc)
write_new(S/'refinement-map.json',{'date':datetime.now(timezone.utc).isoformat(),
 'preserved_prior_authored_drafts':'measurement/M-POC1B-001/initial-authored/',
 'operations':['add DEP-NEW-002 Leader Elephant exception relation','add DEP-NEW-003 Scorpio target exclusion need',
               'add reciprocal assessment traceability and separate relation-basis/target/necessity statuses'],
 'original_source_inventory_candidates_owner_review_modified':False,
 'authoring_note':'Refinement before delivery, no extraction response or owner acceptance exists.'})

# Read actual PDF directly, retain only scoped chapter crops and their separate context.
# Existing renders inspected in chat are hash-linked to the unchanged PDF manifest.
actual=[]
with pdfplumber.open(Path(read(P/'source/source-v1.json')['source']['path'])) as pdf:
    assert len(pdf.pages)==44
    for n in range(31,38):
        page=pdf.pages[n-1]
        for column,box in [('left',(45,45,297,744)),('right',(315,45,567,744))]:
            if n==31 and column=='left': scope='boundary_context'
            elif n==31:
                box=(315,309.4529,567,744); scope='chapter9_core'
            elif n==37 and column=='right': scope='boundary_context'
            elif n==37:
                box=(45,45,297,392.6396); scope='chapter9_core'
            else: scope='chapter9_core'
            actual.append({'pdf_page':n,'column':column,'scope':scope,
                'bbox_pdf_points':box,'text':page.crop(box).extract_text(x_tolerance=2,y_tolerance=3)})
write_new(S/'direct-pdf-read.json',{'source_sha256':read(P/'source/source-v1.json')['source']['sha256'],
 'method':'pdfplumber0.11.10 direct read; helper only. Existing Poppler full renders visually inspected, full hashes verified.',
 'scope_policy':'Chapter9 cuts preserved; excluded columns separately labeled context; no external page added.',
 'regions':actual})

errors=[]
allids={}
for name,doc in docs.items():
    records=doc[name]
    assert len(records)==len(set(r['id'] for r in records))
    allids[name]={r['id'] for r in records}
    assert len(records)==doc['counts']['total']
    assert doc['counts']['owner_confirmed']==0 and not doc['human_review']['approved_ids']
    for r in records:
        assert not r['owner_confirmed'] and r['human_review_status']=='waiting_review'
        assert r['criticality'] in {'critical','noncritical'} and r['criticality_reason']
        assert r['evidence']
        for e in r['evidence']:
            assert e['inventory_ref'] in items
            assert e['source_sha256']==doc['source_sha256']
            assert e['pdf_page'] in range(31,38)
            assert sha(P/e['render'])==e['render_sha256']
            box=e['bbox_pdf_points']
            assert 0<=box[0]<box[2]<=612 and 0<=box[1]<box[3]<=792
            if e.get('helper_lines_inclusive'):
                lo,hi=e['helper_lines_inclusive']
                lines=(P/e['helper_file']).read_text(encoding='utf-8').splitlines()
                expected='\n'.join(lines[lo-1:hi])
                assert expected==e['transcription'], (r['id'],e['inventory_ref'])
    for status,ids in doc['sets'].items():
        if status=='owner_confirmed': assert not ids
        else: assert set(ids)=={r['id'] for r in records if r['status']==status}

def normalize(t): return re.sub(r'\s+',' ',t)
for exp in docs['expectations']['expectations']:
    assert set(exp['dependency_ids'])<=allids['dependencies']
    assert set(exp['situation_ids'])<=allids['situations']
    for e in exp['evidence']:
        if 'source_span' in e:
            combined='\n'.join(x.get('transcription','') for x in items[e['inventory_ref']]['evidence'])
            assert normalize(e['source_span']) in normalize(combined), exp['id']
for sit in docs['situations']['situations']:
    assert sit['expected']['result'] and sit['expected']['rationale']
    assert set(sit['expectation_ids'])<=allids['expectations']
    assert set(sit['dependency_ids'])<=allids['dependencies']
    if sit['expected']['kind']=='justified_block':
        assert sit['expected']['missing_context'] and sit['expected']['blocker']
for dep in deps:
    if dep['to'] and dep['kind']!='continuation': assert dep['to'] in items
    if dep['status'] in {'requires_context','unresolved_interpretation'}: assert dep['missing_target_effect']
    if dep['kind']=='mention': assert not dep['executable'] and dep['criticality']=='noncritical'
    if dep['kind']=='continuation': assert dep['from']!=dep['to'] and not dep['executable']
    assert set(dep['expectation_ids'])<=allids['expectations']
    assert set(dep['situation_ids'])<=allids['situations']
assert len(docs['dependencies']['candidate_audit'])==96
assert {r['candidate_id'] for r in depdoc['candidate_audit']}=={r['id'] for r in read(D/'dependency-candidates.json')['candidates']}
for row in depdoc['candidate_audit']: assert set(row['dependency_ids'])<=allids['dependencies']
assert len(docs['situations']['situations'])==20
assert Counter(r['expected']['kind'] for r in docs['situations']['situations'])=={'local_result':16,'justified_block':4}
assert all(not doc['frozen'] and not doc['gold'] for doc in docs.values())
baseline=read(S/'baseline.json')
for row in baseline['protected_files']:
    p=Path(row['path'])
    assert p.exists() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'], p

# Verify inherited historical-byte protection. No legacy code is executed or imported.
history=read(P/'source/review-evidence/historical-baseline.json')
for row in history:
    p=ROOT/row['path']
    assert p.exists() and p.stat().st_size==row['bytes'] and sha(p)==row['sha256'], p
result={'status':'passed','checked_at_utc':datetime.now(timezone.utc).isoformat(),
 'expectations':docs['expectations']['counts'],'dependencies':depdoc['counts'],
 'relation_denominators':den,'situations':docs['situations']['counts'],
 'expected_kinds':docs['situations']['expected_kind_counts'],'source_actual_PDF_read':True,
 'helper_transcriptions_and_render_hashes':'passed','IDs_links_counts_review_separation':'passed',
 'protected_preexisting_files_unchanged':len(baseline['protected_files']),
 'historical_files_hashes_unchanged':len(history),'Git_index_unchanged':True,
 'no_eval_v1':not (P/'evaluation/eval-v1').exists(),'source_hash':docs['expectations']['source_sha256'],
 'audit_scope':'Artifact integrity/traceability only; cannot confer semantic acceptance.'}
write_new(S/'artifact-audit.json',result)
print(json.dumps(result,ensure_ascii=False))
