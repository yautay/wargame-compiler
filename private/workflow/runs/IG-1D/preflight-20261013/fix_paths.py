from pathlib import Path
import json
R=Path(__file__).parent;ROOT=Path.cwd()
p=R/'ready.json';e=json.loads(p.read_text())
for a in e['artifacts']:
 if Path(a['path']).is_absolute():a['path']=Path(a['path']).relative_to(ROOT).as_posix()
with (R/'ready-02.json').open('x',encoding='utf-8',newline='\n') as f:json.dump(e,f,indent=2);f.write('\n')
qpath=Path('docs/work/queue.json');q=json.loads(qpath.read_text());t=next(t for t in q['tasks'] if t['id']=='IG-1D');assert t['status']=='planned'
root=ROOT.as_posix()+'/'
t['inputs']=[s[len(root):] if s.startswith(root) else s for s in t['inputs']]
if t['export_profile_decision']['path'].startswith(root):t['export_profile_decision']['path']=t['export_profile_decision']['path'][len(root):]
with qpath.open('w',encoding='utf-8',newline='\n') as f:json.dump(q,f,ensure_ascii=False,indent=2);f.write('\n')
with (R/'path-correction.json').open('x',encoding='utf-8',newline='\n') as f:json.dump({'failure':'First ready evidence incorrectly used absolute repository-local artifact paths; workflow safe-path guard correctly refused readiness.','changed_condition':'Normalize only repository-local artifacts/input pins to root-relative POSIX paths and preserve first evidence as ready.json. Use new ready-02.json. No product edits or gate weakening.'},f,indent=2);f.write('\n')
