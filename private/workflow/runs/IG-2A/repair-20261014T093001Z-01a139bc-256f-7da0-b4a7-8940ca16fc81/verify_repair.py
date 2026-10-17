"""Fresh derivations, migrated review probes and independent pixel oracles."""
import copy
import importlib.util
import json
import logging
import sys
from pathlib import Path
from prepare import ROOT, RUN, OLD, REVIEW, sha, write, pin, command
from wgc.contracts.source import canonical_bytes
from wgc.sources.inventory import seal, validate, partition_hash, page_basis_hash
from wgc.sources.pdf import extract_evidence

logging.basicConfig(filename=RUN/'pypdf-warnings.log',level=logging.WARNING)

def reseal(doc):
    doc['pages']=[seal(p) for p in doc['pages']]
    doc['regions']=[seal(r) for r in doc['regions']]
    return seal(doc)

def probes():
    p=RUN/'probes'; p.mkdir(exist_ok=False); rel=p.relative_to(ROOT).as_posix()
    oldbase=json.loads((REVIEW/'p2/baseline.input.json').read_text())
    baseline=copy.deepcopy(oldbase); baseline['evidence']=[]
    for page in baseline['pages']:
        if page['label']['status']=='verified':
            page['label']={'status':'unknown','value':None,'reason':'Fresh evidence association pending','evidence':None}
    baseline=reseal(baseline)
    fresh=[]
    for i,old_ev in enumerate(oldbase['evidence']):
        fresh.append(extract_evidence(baseline,old_ev['region_id'],ROOT,f'{rel}/e{i}'))
    evmap={e['id']:f for e,f in zip(oldbase['evidence'],fresh)}
    baseline['evidence']=fresh; baseline=seal(baseline); validate(baseline,ROOT)
    exact=json.loads((REVIEW/'p2/exact_exclusion_claim.input.json').read_text())
    exact['evidence']=[]
    for r in exact['regions']:
        for cov in r['coverage'].values():
            if cov['boundary']: cov['boundary']['partition_hash']=partition_hash(exact)
    exact=reseal(exact); validate(exact,ROOT)
    exact_basis=partition_hash(exact)
    # Fresh baseline and decision scope are explicit migration steps, not changed expectations.
    write('probe-migration.json',{'prior_baseline':pin(REVIEW/'p2/baseline.input.json'),
          'fresh_evidence':fresh,'prior_exact_exclusion':pin(REVIEW/'p2/exact_exclusion_claim.input.json'),
          'migrated_exclusion_scope':exact_basis,'human_authority':'Synthetic fixture; not authenticated'})
    names=['stale_page_rotation','stale_page_userunit','stale_page_crop','false_render_dpi','wrong_page_printed_label',
           'exclusion_after_region_revision','exclusion_after_registry_change','exclusion_after_page_remap',
           'false_consistent_page_count','physical_page_remapping']
    cases=[('fresh_baseline',baseline,True),('migrated_exact_exclusion',exact,True)]
    for name in names:
        doc=json.loads((REVIEW/'p2'/(name+'.input.json')).read_text())
        for i,e in enumerate(doc['evidence']):
            old=copy.deepcopy(e); replacement=copy.deepcopy(evmap[e['id']])
            if name=='false_render_dpi': replacement['render_parameters']['dpi']=old['render_parameters']['dpi']
            doc['evidence'][i]=replacement
        for page in doc['pages']:
            if page['label']['status']=='verified': page['label']['evidence']=evmap[page['label']['evidence']]['id']
        for r in doc['regions']:
            for cov in r['coverage'].values():
                if cov['boundary']: cov['boundary']['partition_hash']=exact_basis
        cases.append((name,reseal(doc),False))
    reordered=copy.deepcopy(baseline); reordered['pages'].reverse()
    cases.append(('reordered_page_array',seal(reordered),True))
    forged=copy.deepcopy(baseline); forged['pages'][0]['rotation']=180
    forged['evidence'][0]['page_basis_hash']=page_basis_hash(forged['pages'][0])
    cases.append(('forged_geometry_and_evidence_basis',reseal(forged),False))
    for field,value in [('kind','diagram'),('uncertainty',['Changed separate uncertainty']),('key','rekeyed')]:
        doc=copy.deepcopy(exact); region=doc['regions'][0]; old_key=region['key']; region[field]=value
        if field=='key': next(e for e in doc['registry']['entries'] if e['kind']=='region' and e['key']==old_key)['key']=value
        cases.append(('exclusion_changed_'+field,reseal(doc),False))
    records=[]
    for name,doc,expected in cases:
        path=p/(name+'.json'); path.write_bytes(canonical_bytes(doc)+b'\n')
        try: report=validate(doc,ROOT); error=None; actual=True
        except ValueError as exc: report=None; error=str(exc); actual=False
        records.append({'name':name,'input':pin(path),'expected':'accept' if expected else 'reject',
                        'actual':'accept' if actual else 'reject','error':error,'report':report,'passed':expected==actual})
    write('repair-probes.json',{'cases':records,'total':len(records),'unmet':sum(not r['passed'] for r in records)})
    assert all(r['passed'] for r in records),records
    print('Fresh baseline and all migrated/own probe expectations passed:',len(records))

def inventories():
    src='private/ig/sources/spqr-5e-official/revision-20261013T155212Z'
    rel=RUN.relative_to(ROOT).as_posix()
    registry='private/ig/projects/spqr/sources/inventory/ig2a-20261013T155212Z/seed/identity-registry.json'
    args=[sys.executable,'-m','wgc.sources','inventory','--pdf',src+'/rulebook.pdf','--provenance',src+'/provenance.json',
          '--source-id','source:spqr:5e:core','--sha256','e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e']
    for name,reg in [('inventory-one',registry),('inventory-two',rel+'/inventory-one/identity-registry.json')]:
        result=command(name,args+['--registry',reg,'--output',rel+'/'+name]); assert result['exit_code']==0
    one=RUN/'inventory-one/inventory.json'; two=RUN/'inventory-two/inventory.json'
    a=json.loads(one.read_text()); b=json.loads(two.read_text()); assert one.read_bytes()==two.read_bytes()
    assert a['registry']==b['registry']==json.loads((ROOT/registry).read_text())
    assert one.read_bytes()==(ROOT/'private/ig/projects/spqr/sources/inventory/ig2a-20261013T155212Z/seed/inventory.json').read_bytes()
    write('repeatability.json',{'inventories':[pin(one),pin(two)],'canonical_bytes_identical':True,
          'identities_identical':True,'frozen_seed_bytes_identical':True,'page_count':44,
          'represented_regions':0,'substantive_inventory':'Pending IG-2B; not executed'})
    result=command('real-evidence',[sys.executable,'-m','wgc.sources','evidence','--inventory',rel+'/inventory-one/inventory.json',
                                  '--pages','1','2','3','4','--output',rel+'/real-evidence']); assert result['exit_code']==0
    # Preserve and apply only the previously recorded observations on unchanged pages 1-4.
    fresh=json.loads((RUN/'real-evidence/inventory.json').read_text())
    prior=json.loads((ROOT/'private/ig/projects/spqr/sources/inventory/ig2a-20261013T155212Z/verified-inventory.json').read_text())
    for page in fresh['pages']:
        old=next(p for p in prior['pages'] if p['id']==page['id'])
        if old['label']['status']=='verified':
            newev=next(e for e in fresh['evidence'] if e['page_id']==page['id']); oldev=next(e for e in prior['evidence'] if e['page_id']==page['id'])
            assert newev['image']['sha256']==oldev['image']['sha256']
            page['label']=copy.deepcopy(old['label']); page['label']['evidence']=newev['id']
    fresh=reseal(fresh); report=validate(fresh,ROOT)
    (RUN/'verified-inventory.json').write_bytes(canonical_bytes(fresh)+b'\n')
    write('verified-coverage.json',report)
    write('label-observation-provenance.json',{'basis':pin(ROOT/'private/ig/projects/spqr/sources/inventory/ig2a-20261013T155212Z/verified-inventory.json'),
          'scope':'Previously recorded visual labels 2/3/4 only; exact fresh PNG bytes equal previous PNGs; current executor inspection recorded separately',
          'semantic_acceptance_granted':False})

def oracle():
    # Execute the sealed review's independent numerical/pixel oracle in this new run.
    # Only output destinations and the current inventory path differ.
    text=(REVIEW/'audit.py').read_text()
    text=text.replace("doc=json.loads((INV/'verified-inventory.json').read_text());validate(doc,ROOT)",
                      "doc=json.loads((OUT/'verified-inventory.json').read_text());validate(doc,ROOT)")
    target=RUN/'source_and_pixel_oracle.py'; target.write_text(text,encoding='utf-8',newline='\n')
    write('oracle-adaptation.json',{'original':pin(REVIEW/'audit.py'),'adapted':pin(target),
          'change':'OUT follows this new file; current verified-inventory.json replaces old inventory; all geometry/pixel expectations and source access limits unchanged'})
    result=command('source-and-pixel-oracle',[sys.executable,str(target)]); assert result['exit_code']==0
    print((RUN/'source-and-pixel-oracle.stdout').read_text())

if __name__=='__main__':
    probes(); inventories(); oracle()
