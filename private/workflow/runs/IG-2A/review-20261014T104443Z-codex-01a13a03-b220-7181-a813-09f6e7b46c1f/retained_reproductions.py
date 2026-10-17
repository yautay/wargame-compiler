from support import *
import copy
from wgc.sources import inventory as inv
from wgc.sources.pdf import extract_evidence
base=read(PRIOR/'p2/baseline.input.json')
assert all('page_basis_hash' not in e for e in base['evidence'])
old_base=copy.deepcopy(base);base['evidence']=[];base=inv.seal(base)
# Fresh derivation rather than treating schema-only rejection as finding closure.
base['evidence']=[extract_evidence(base,r['id'],ROOT,(RUN/f'migrated-evidence-{i}').relative_to(ROOT).as_posix()) for i,r in enumerate(base['regions'])]
base=inv.seal(base);inv.validate(base,ROOT)
results=[]
names=['stale_page_crop','stale_page_rotation','stale_page_userunit','false_render_dpi','wrong_page_printed_label','exclusion_after_region_revision','exclusion_after_registry_change','exclusion_after_page_remap','false_consistent_page_count','physical_page_remapping']
for name in ['baseline','exact_exclusion_claim']+names:
    old=read(PRIOR/f'p2/{name}.input.json');d=copy.deepcopy(old)
    # Migrate the exact old candidate mutation onto freshly derived evidence, keeping
    # baseline page basis pins. False DPI and cross-page label mutations remain intact.
    for e in d['evidence']:
        old_ev=next(x for x in old_base['evidence'] if x['id']==e['id'])
        fresh=next(x for x in base['evidence'] if x['region_id']==e['region_id'])
        for field in ['page_basis_hash','crop_pdf','text','image']:
            e[field]=fresh[field]
        # Keep legacy evidence ID references: IDs are local locators, not canonical hashes.
    # Old exact exclusion's rectangle-only hash is migrated to the unmodified author
    # scope; changed author/registry/physical basis must not get a newly approved hash.
    old_excluded=read(PRIOR/'p2/exact_exclusion_claim.input.json')
    reference_scope=inv.partition_hash(old_excluded)
    for r in d['regions']:
        for cov in r['coverage'].values():
            if cov['boundary'] is not None:cov['boundary']['partition_hash']=reference_scope
    d['pages']=[inv.seal(p) for p in d['pages']];d['regions']=[inv.seal(r) for r in d['regions']];d=inv.seal(d)
    candidate=write('retained/'+name+'.json',d);start,t=utc(),time.monotonic()
    try:report=inv.validate(d,ROOT);actual='accept';error=None
    except Exception as exc:report=None;actual='reject';error=type(exc).__name__+': '+str(exc)
    expected='accept' if name in ['baseline','exact_exclusion_claim'] else 'reject'
    results.append({'name':name,'original_candidate':pin(PRIOR/f'p2/{name}.input.json'),'candidate':pin(candidate),'expected':expected,'actual':actual,'error':error,'report':report,'expectation_met':expected==actual and (error is None or 'inventory schema:' not in error),'started_utc':start,'ended_utc':utc(),'wall_seconds':time.monotonic()-t})
    print(name,actual,error or '')
write('retained-reproduction-results.json',{'migration':'Fresh baseline derivation; source geometry unchanged; old adverse mutations retained; exclusion scope migrated only from unchanged exact baseline. No old file modified.','results':results})
assert all(x['expectation_met'] for x in results)
