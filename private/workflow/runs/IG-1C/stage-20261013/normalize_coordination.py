"""Preserve baseline line endings; new coordinator lines use LF for diff checks."""
from pathlib import Path
import difflib, json, sys
sys.path.insert(0,'scripts')
import workflow
run=Path(__file__).parent
before=json.loads((run/'queue-before.json').read_text())
current=workflow.read_json('docs/work/queue.json')
oldviews=workflow.views(before)
for name in ['docs/work/queue.json',*workflow.views(current)]:
    p=Path(name)
    new=p.read_text(encoding='utf-8').splitlines(keepends=True)
    if name=='docs/work/queue.json':
        old=json.dumps(before,ensure_ascii=False,indent=2).splitlines(keepends=True)
        if not old[-1].endswith('\n'):old[-1]+='\n'
        crlf=True
    else:
        old=oldviews[name].splitlines(keepends=True)
        crlf=name in ['docs/STATUS.md','docs/HANDOFF.md','docs/work/tasks/IG-1A.md','docs/work/tasks/IG-1B.md']
    out=[]
    for op,i,j,a,b in difflib.SequenceMatcher(a=old,b=new,autojunk=False).get_opcodes():
        if op=='equal':out.extend(x.replace('\n','\r\n') if crlf else x for x in old[i:j])
        elif op in ('replace','insert'):out.extend(new[a:b])
    p.write_bytes(''.join(out).encode('utf-8'))
