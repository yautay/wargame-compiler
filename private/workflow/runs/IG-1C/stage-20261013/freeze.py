"""Freeze current IG-1C delivery; no acceptance implied."""
import hashlib, json, sys, zipfile
from datetime import datetime,timezone
from pathlib import Path
R=Path(__file__).parent
ROOT=Path.cwd()
def sha(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def write(name,data):
 with (R/name).open('x',encoding='utf-8',newline='\n') as f:json.dump(data,f,indent=2);f.write('\n')
installed=[]
with zipfile.ZipFile(R/'dependencies/pyyaml-6.0.3-cp312-cp312-win_amd64.whl') as wheel:
 for name in wheel.namelist():
  if name.endswith('/') or name.endswith('/RECORD'):continue
  path=Path(sys.prefix)/'Lib/site-packages'/name
  assert path.read_bytes()==wheel.read(name),name
  installed.append({'path':str(path),'sha256':sha(path)})
write('installed-dependency-audit.json',{'all_wheel_files_match':True,'files':installed,'record_note':'pip rewrites dist-info/RECORD during installation; excluded from literal wheel equality; source/extension/metadata bytes match.'})
checks=[{'command':'.venv/Scripts/python.exe -m pytest tests/wgu_adapter -q -p no:cacheprovider --basetemp private/workflow/checks/c2 --tb=short','exit_code':0,'tests_passed':31,'reported_seconds':0.68}, {'command':'.venv/Scripts/python.exe private/workflow/runs/IG-1C/stage-20261013/full_audit.py (authorized native handle escalation)','exit_code':0,'independent_report':'private/ig/projects/spqr/runs/import/ig1c-20261013/independent-accounting.json'}, {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-1C','exit_code':0,'tests_passed':102,'reported_seconds':75.53,'result':'private/workflow/checks/active-34524a59441f41569faf8bd8a244281d/result.json'}, {'command':'git diff --check','exit_code':0}]
write('checks.json',checks)
report='''# IG-1C technical delivery

Complete lossless import of the frozen WGU input preserves raw bytes, YAML field
locations, extensions, file metadata, unknown files and nested records. Safe YAML
loading rejects unsafe tags, duplicate keys, recursive aliases, unsupported complex
keys/merge keys and over-budget input explicitly. Malformed records remain in the
ledger with errors. Anonymous terms and nested step numbers retain their original
values. Duplicate recognized entity IDs retain every occurrence and diagnostic.
Auxiliary game identifiers are metadata, not entity identities.

The independent full-input oracle reads the manifest and files directly, inventories
every record and every field separately from adapter counters, compares all values
and raw bytes and verifies two complete imports are byte-identical. It measures 59
manifest entries: 23 available WGU files (1,233,389 bytes), 36 unavailable configured
sources; 1,692 accounted records: 1,655 processed, 37 raw, zero errors; 38,206 YAML
field/container locations. The separately pinned registry contains two available
files, bringing foundation available bytes to 5,199,801. The PDF is not KB data.

Recognized records: 523 rules, 134 terms, 15 procedures, 80 steps, 48 tables, 233
relations, 79 ambiguities, 3 changes, 59 evaluation questions, 465 terminology
concepts, 16 confusables. Auxiliary records account for all remaining file metadata.
Counts are measured and independently derived, not historical test constants.

Refs/see are navigation only. Relation verified, table complete, ambiguity resolved,
terminology decisions and question answers retain imported values without approval.
No publisher-source coverage, human semantic acceptance, executable readiness or
game interpreter is claimed. Missing/mixed-edition materials remain for later
reconciliation. Source identity to WGU's missing original remains unknown.

Dependency: project-local PyYAML 6.0.3; wheel SHA-256 matches saved official PyPI
metadata; installed wheel source/extension files match literally. Product scope is
parser.py/importer.py/tests and private import runs; dependency installation is the
operator-authorized separate .venv exception. No foundation product edits.

Controls: 31 synthetic adapter tests and 102 existing project tests pass; full
private file/record/field accounting and repeatability pass; diff check passes.
Native no-follow handle verification required narrowly approved local escalation
because sandbox denied GetFinalPathNameByHandle (WinError 5). Symlink behavior is
unmeasured here; prior unavailable native symlink measurements remain null.
Initial harness assertions used differing IG-1A review field/case conventions and
were corrected against actual evidence. First full audit exposed the shared game-ID
bug; a regression closes it. Initial project check failed solely on coordinator
CRLF diff whitespace. Baseline line endings are preserved and added lines use LF.
All prior reports/accepted foundation files remain unchanged.

Independent technical review is pending. IG-1D and IG-1E remain planned. Operator
confirmed this executor conversation's UI as "sol 6.1 high"; requested reviewer
settings do not establish actual reviewer configuration. Usage/cost/operator time
are unavailable and null.
'''
(R/'report.md').write_bytes(report.encode('utf-8'))
q=json.loads(Path('docs/work/queue.json').read_text());t=next(t for t in q['tasks'] if t['id']=='IG-1C')
checkpoint=json.loads((R/'checkpoint.json').read_text())
ended=datetime.now(timezone.utc)
write('measurement.json',{'started_utc':checkpoint['started_utc'],'ended_utc':ended.isoformat(),'wall_seconds':(ended-datetime.fromisoformat(checkpoint['started_utc'])).total_seconds(),'interval':'Claim-to-frozen-delivery wall interval; includes tool waits','input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,'native_file_symlink':None,'native_directory_symlink':None})
paths=[Path('src/wgc/wgu_adapter/parser.py'),Path('src/wgc/wgu_adapter/importer.py'),Path('tests/wgu_adapter/test_importer.py')]
paths+=sorted(p for p in R.rglob('*') if p.is_file() and '__pycache__' not in p.parts)
paths+=sorted(Path('private/ig/projects/spqr/runs/import/ig1c-20261013').glob('*.json'))
check=Path('private/workflow/checks/active-34524a59441f41569faf8bd8a244281d')
paths+=sorted(p for p in check.glob('*') if p.is_file())
artifacts=[{'path':p.relative_to(ROOT).as_posix() if p.is_absolute() else p.as_posix(),'sha256':sha(p)} for p in paths]
write('delivery.json',{'role':'executor','actor':'ig1-stage-executor-20261013','task':'IG-1C','summary':'Complete structural WGU import: all 23 available input files and 1692 records independently accounted; 38206 fields preserved; two imports byte-identical; 31 adapter and 102 project tests pass. Independent review pending.','criteria':t['acceptance'],'artifacts':artifacts,'checks':checks,'model':'gpt-6.1-sol','reasoning':'high','configuration_evidence':{'path':R.relative_to(ROOT).as_posix()+'/configuration.json','sha256':sha(R/'configuration.json'),'source':'Direct current-session operator UI confirmation'},'input_packet':checkpoint['input_packet'],'unmet_lifecycle_gates':['Independent technical review','Coordinator acceptance/done'],'semantic_acceptance_granted':False,'source_coverage_granted':False,'executable_readiness_granted':False})
print('Delivery frozen',len(artifacts),'artifacts',sha(R/'delivery.json'))
