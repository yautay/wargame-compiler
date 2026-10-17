"""Review current frozen ledgers and exact replay output sets, without dependency dumps."""
import copy
import hashlib
import importlib.metadata
import json
import os
from pathlib import Path
from wgc.sources.inventory import seal, digest

R = Path(__file__).parent
A = Path('private/workflow/runs/IG-2B07/inventory-25-28-01')
S = Path('private/workflow/orchestrator/20261016T195516Z-332903f5/003-IG-2B07-reviewer-3f57d66e')
def load(p): return json.loads(Path(p).read_text(encoding='utf-8'))
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def normalize(v, prefix):
    if isinstance(v, str): return '$RUN/' + v[len(prefix)+1:] if v.startswith(prefix+'/') else v
    if isinstance(v, list): return [normalize(x,prefix) for x in v]
    if isinstance(v, dict): return {k:normalize(x,prefix) for k,x in v.items()}
    return v

task=load(S/'task.json')
delivery=load(A/'delivery.json')
packet=load(S/'packet.json')
bootstrap=load(S/'access-manifest.json')['bootstrap_reads']
packet_results=[]
for item in packet['files'] + packet['control_files']:
    pin=bootstrap.get(item['path'],item)
    path=Path(pin['path'])
    assert sha(path)==pin['sha256'] and path.stat().st_size==pin['bytes'],item['path']
    packet_results.append(item['path'])
assert delivery['criteria']==task['acceptance']
rows=load(A/'region-ledger.json')['regions']
components=load(A/'component-ledger.json')['components']
coverage=load(A/'coverage-report.json')
continuations=load(A/'continuations.json')
final=load(A/'final-verified/inventory.json')
byid={x['id']:x for x in final['regions']}
evidence={x['region_id']:x for x in final['evidence']}
newids={x['region']['id'] for x in rows}
componentids={x['region']['id'] for x in components}
assert len(rows)==len(newids)==188 and len(componentids)==86
assert components==[{k:v for k,v in x.items() if k!='reading_order_index'} for x in rows if x['category']=='component']
for row in rows:
    identity=row['region']['id']
    assert row['region']==byid[identity]
    assert row['evidence']==evidence[identity]
    assert final['reading_order'][row['reading_order_index']]==identity
    assert row['box']==row['region']['box']==row['evidence']['box']
    assert row['evidence']['pdf_page']==row['page']
    if row['category']=='component':
        parent=next(x for x in rows if x['key']==row['parent_key'])
        assert parent['region']['id']==row['parent_region_id']
        x0,y0,x1,y1=parent['box'];a,b,c,d=row['box']
        assert x0<=a<c<=x1 and y0<=b<d<=y1
        assert row['role']=='context'
    elif row['category']=='boundary':
        x0,y0,x1,y1=task['source_scope']['context_only_boxes'][str(row['page'])]
        a,b,c,d=row['box']; assert x0<=a<c<=x1 and y0<=b<d<=y1
        assert row['role']=='context'
    else:
        assert row['page'] in (25,26,27,28) and row['role']=='inventory'
assert set(coverage['assigned_inventory_ids'])=={x['region']['id'] for x in rows if x['role']=='inventory'}
assert set(coverage['new_nested_component_ids'])==componentids
assert set(coverage['new_boundary_ids'])=={x['region']['id'] for x in rows if x['category']=='boundary'}
assert set(coverage['full_inventory_ids'])=={x['id'] for x in final['regions'] if x['denominator_role']=='inventory'}
assert set(coverage['full_context_ids'])=={x['id'] for x in final['regions'] if x['denominator_role']=='context'}
assert coverage['context_denominator_contribution']==0
assert {x['id'] for x in continuations['endpoints']}==newids
assert final['links'][158:]==continuations['links']
assert digest(final['links'][:158])==continuations['inherited_links_exact']['canonical_sha256']
for old in load(A/'region-ledger.json')['preserved_nonassigned_index']:
    assert all(byid[old['id']][k]==v for k,v in old.items())
retired=set(task['source_scope']['replace_only_region_ids'])
assert not retired & set(byid)
assert retired <= {x['id'] for x in final['registry']['entries']}
assert final['registry']==load(A/'final-verified/identity-registry.json')
sheetids=[i for x in load(A/'original-page-inspection.json')['fresh_region_component_sheets'] for i in x['region_ids']]
assert len(sheetids)==len(set(sheetids))==188 and set(sheetids)==newids
normalized=[]
for name in ('final-verified','replay-1','replay-2'):
    directory=A/name
    doc=load(directory/'inventory.json')
    report=load(directory/'derivation-report.json')
    assert set(report['complete_target_ids'])==newids
    assert set(report['component_ids'])==componentids
    assert len(report['invocations'])==188 and all(x['exit_code']==0 for x in report['invocations'])
    normalized.append(seal(normalize(doc,directory.as_posix())))
assert normalized[0]==normalized[1]==normalized[2]
tc=load(A/'toolchain.json')
assert tc['process_pythonpath']==os.environ['PYTHONPATH']
for native in tc['native'].values(): assert sha(native['path'])==native['sha256']
assert all(importlib.metadata.version(k)==v for k,v in tc['libraries'].items())
meta={k:v for k,v in load(R/'checkpoint.json').items() if k in ('role','actor','model','reasoning','configuration_evidence','configuration_sha256')}
report=dict(meta,all_passed=True,packet_files_verified=len(packet_results),frozen_normalized_replays_equal=True,new_region_count=188,component_count=86,assigned_denominator=100,full_denominator=849,full_context_count=91,preserved_index_count=752,retired_placeholder_count=4,source_accounting_completeness='Separate visual review found one missing nested arrow; structural equality is not completeness.',baseline_read_boundary='Accepted dependency pins and prepared projection only; frozen preserved index and inherited-link canonical hash checked internally. No unassigned original source content read.')
(R/'structure-verification.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps(report))
