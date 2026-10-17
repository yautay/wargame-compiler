"""Pin exact accepted IG-1 inputs before readiness; no downstream work."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json
ROOT = Path.cwd(); RUN = Path(__file__).resolve().parent
def sha(p): return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def read(p): return json.loads(Path(p).read_bytes())
def art(p): return {'path': str(p).replace('\\','/'), 'sha256': sha(p)}
def write(n,d):
    with (RUN/n).open('x',encoding='utf-8',newline='\n') as f: json.dump(d,f,indent=2);f.write('\n')
queue_path = Path('docs/work/queue.json'); q = read(queue_path)
task = next(t for t in q['tasks'] if t['id']=='IG-1E')
assert task['status']=='planned'
assert next(t for t in q['tasks'] if t['id']=='IG-1D')['status']=='done'
with (RUN/'queue-before.json').open('xb') as f: f.write(queue_path.read_bytes())
package = 'private/ig/projects/spqr/records/exports/sha256-ba0548e6fd9f650c2295c7bd587e4b1724c8b93e055727feab329fbaece692cc/'
paths = [
 'private/ig/projects/spqr/inputs/sha256-0dedff0ef3588face0e2c26646d4ddea9b7aa05c5acf62d2e43ca6dd462a96df/manifest.json',
 'private/ig/projects/spqr/sources/sha256-86dd7a36afc645e6a82cb3b1d7f3ca22d542af7fdfb01f1a7dc8d0c136699008/manifest.json',
 'private/ig/projects/spqr/runs/import/ig1c-repair01-final-20261013/import.json',
 'private/workflow/runs/IG-1D/repair-02-20261013/delivery.json',
 'private/workflow/runs/IG-1D/repair-02-20261013/preservation.json',
 'private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/review.json',
 'private/workflow/runs/IG-1D/replacement-rereview-20261013T143653Z/review-manifest.json',
 'private/workflow/runs/IG-1D/repair-02-20261013/accounting.py',
 'private/workflow/runs/IG-1D/preflight-20261013/initial-registry.json',
 *[package+n for n in ['manifest.json','source-ig.json','identity-registry.json','references.json']],
 *['src/wgc/'+p for p in ['wgu_adapter/importer.py','wgu_adapter/parser.py','wgu_adapter/identity.py',
                         'wgu_adapter/references.py','export/source.py','export/storage.py',
                         'export/source-export.schema.json','inputs/snapshot.py','contracts/source.py']]
]
pins = [art(p) for p in paths]
for t in q['tasks']:
 if t['id'] in ['IG-1A','IG-1B','IG-1C','IG-1D']:
  assert t['status']=='done'
  accepted=read(next(e['evidence'] for e in reversed(t['events']) if e['to']=='accepted'))
  for a in accepted['artifacts']: assert sha(a['path'])==a['sha256'],a['path']
contract = {'task':'IG-1E','pinned_inputs':pins,
 'context_scope':'Read only exact frozen manifest-enumerated blobs, accepted import/package and pinned adapter/contract modules. No neighboring repository, archive, Git history or publisher text inspection.',
 'outputs':['tests/integration/', 'private/ig/projects/spqr/runs/import-acceptance/ig1e-20261013/', 'private/ig/projects/spqr/snapshots/'],
 'independent_oracle':'Re-enumerate exact files and raw YAML entities/fields independently; compare complete path/key sets and processed/raw/error counts, unknown payloads, bindings and hash/revision closure; do not trust importer counters.',
 'reproducibility':'Two new complete imports must equal each other and accepted IG-1C bytes; two complete canonical transforms/publications must equal accepted IG-1D draft; two sealed snapshots must be byte-identical.',
 'seal_contract':'New content-addressed snapshot identity with state sealed and a historical lineage reference to retained exact draft snapshot. Preserve all selected revisions, gaps, profiles, missing sources, mixed-edition uncertainty and readiness assessments. Original draft bundle remains unchanged. Sealed refers only to structural integrity.',
 'snapshot_storage':'Dedicated wgc-structural-snapshot-1 manifest and immutable content-addressed directory under snapshots; canonical timestamps remain null, operational timestamps/actual configuration in sidecars. Existing draft-package publisher is unchanged.',
 'semantic_acceptance_required':False,'semantic_acceptance_granted':False}
write('input-contract.json',contract)
task['inputs']=[p['path']+' SHA-256 '+p['sha256'] for p in pins]+[
 'Use only exact files enumerated by the frozen input/source manifests; no publisher text/page interpretation.',
 'Independent complete inventory, two fresh imports/transforms/publications and reproducible sealed structural snapshot; no semantic, source-coverage or executable acceptance.',
 'New sealed snapshot identity retains original draft snapshot by exact historical lineage and preserves every selected revision/readiness assessment; immutable dedicated structural manifest, no existing profile/schema changes.']
task['context'] += ['contracts/ig/README.md','src/wgc/contracts/source.py','src/wgc/export/README.md']
queue_path.write_text(json.dumps(q,ensure_ascii=False,indent=2)+'\n',encoding='utf-8',newline='\n')
write('ready.json',{'role':'coordinator','actor':'ig1-continuation-executor-20261013',
 'summary':'IG-1D is accepted/done; exact frozen inputs, allowed raw-byte scope, independent accounting, reproducibility and structural seal contract pinned for IG-1E.',
 'criteria':task['acceptance'],'artifacts':[art('private/workflow/runs/IG-1E/stage-20261013/input-contract.json')],
 'model':'gpt-6.1-sol','reasoning':'high',
 'configuration_evidence':art('private/workflow/runs/IG-1D/resume-audit-20261013T134548Z/configuration-confirmed.json'),
 'recorded_utc':datetime.now(timezone.utc).isoformat()})
print('IG-1E exact contract refined; statuses unchanged; readiness evidence prepared.')
