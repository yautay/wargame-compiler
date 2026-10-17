"""Prepare independent IG-1E review without writing into frozen acceptance run."""
import ast
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[5]
RUN = Path(__file__).resolve().parent
STAGE = ROOT / 'private/workflow/runs/IG-1E/stage-20261013'
ACTOR = 'ig1e-independent-reviewer-20261013T150750Z'
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def write(n,d):
    with (RUN/n).open('x',encoding='utf-8') as f: json.dump(d,f,indent=2);f.write('\n')
config = ROOT / 'private/workflow/runs/IG-1D/replacement-rereview-20261013T140127Z/configuration-confirmed.json'
write('checkpoint.json',{'role':'reviewer','actor':ACTOR,'task':'IG-1E','started_utc':datetime.now(timezone.utc).isoformat(),
    'measurement_scope':'Fresh evidence run; earlier instruction reading not timed.',
    'model':'gpt-6.1-sol','reasoning':'high','same_reviewer_chat_continuity':True,
    'configuration_evidence':{'path':config.relative_to(ROOT).as_posix(),'sha256':sha(config)},
    'tokens':None,'cost':None,'operator_seconds':None})
raw = (STAGE/'accounting.py').read_bytes()
assert sha(STAGE/'accounting.py') == '513626629608567510faf6243afc5565aa93f4c66827a4213f8c41d3193e0a99'
adapted = raw.replace(b"RUN = ROOT / 'private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013'", b'RUN = Path(__file__).resolve().parent')
adapted = adapted.replace(b"'executor_actor': 'ig1-continuation-executor-20261013'", ("'review_actor': '"+ACTOR+"'").encode())
adapted = adapted.replace(b"{'ledger', 'binding_ledger', 'unknown_locations', 'publications'}", b"{'ledger', 'binding_ledger', 'unknown_locations', 'publications', 'independent_unknown_roots', 'independent_unknown_field_locations'}")
old_asserts=[ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(raw)) if isinstance(n,ast.Assert)]
new_asserts=[ast.dump(n,include_attributes=False) for n in ast.walk(ast.parse(adapted)) if isinstance(n,ast.Assert)]
assert old_asserts==new_asserts
with (RUN/'accounting.py').open('xb') as f:f.write(adapted)
supp_source=ROOT/'private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/supplemental_audit.py'
with (RUN/'supplemental_audit.py').open('xb') as f:f.write(supp_source.read_bytes())
write('helper-provenance.json',{'source':{'path':(STAGE/'accounting.py').relative_to(ROOT).as_posix(),'sha256':sha(STAGE/'accounting.py')},
    'copy':{'path':(RUN/'accounting.py').relative_to(ROOT).as_posix(),'sha256':sha(RUN/'accounting.py')},
    'assertion_count':len(old_asserts),'all_assertion_ASTs_exactly_equal':True,
    'only_deltas':['RUN output destination','Operational actor key/value','Exclude large arrays from stdout only'],
    'supplemental_source':{'path':supp_source.relative_to(ROOT).as_posix(),'sha256':sha(supp_source)},'supplemental_exact_copy':True})
print(json.dumps({'run':str(RUN),'preserved_assertions':len(old_asserts)}))
