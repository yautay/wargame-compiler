"""Local planning controls. No game implementation and no model/network execution."""
from __future__ import annotations

import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import re
import sys
import uuid

ROOT = Path(__file__).resolve().parents[1]
QUEUE = 'docs/work/queue.json'
TRANSITIONS = {
    'planned': {'ready', 'blocked'}, 'ready': {'in_progress', 'blocked'},
    'in_progress': {'review', 'blocked'}, 'review': {'changes_requested', 'accepted', 'blocked'},
    'changes_requested': {'in_progress', 'blocked'}, 'accepted': {'done', 'changes_requested'},
    'blocked': {'planned'}, 'done': {'planned'},
}
BUSY = {'in_progress', 'review', 'changes_requested', 'accepted'}
DENIED = ('archive', 'private/archive', 'docs/adr', 'docs/reviews',
          'docs/prompts', 'docs/handoff', 'docs/POC-PLAN.md', 'docs/SESSION-PLAYBOOK.md',
          'docs/LESSONS-LEARNED.md', 'docs/work/tasks/README.md', 'docs/work/tasks/IG-0.md', 'private/ig/migration',
          'private/ig/research', 'private/ig/reviews', 'private/ig/_checks', '.git', '.venv')
BASE_CONTEXT = ['AGENTS.md', 'README.md', 'docs/STATUS.md', 'docs/HANDOFF.md',
                'docs/work/WORKFLOW.md', 'docs/skills/wgc-execute/SKILL.md']

def read_json(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def digest(path):
    with Path(path).open('rb') as stream:
        return hashlib.file_digest(stream, 'sha256').hexdigest()

def safe_path(root, rel):
    if not rel or '\\' in rel or ':' in rel or Path(rel).is_absolute() or '..' in Path(rel).parts:
        raise ValueError(f'Unsafe relative path: {rel}')
    path = root / rel
    cursor = path
    while cursor != root:
        if cursor.is_symlink() or (hasattr(cursor, 'is_junction') and cursor.is_junction()):
            raise ValueError(f'Linked path: {rel}')
        cursor = cursor.parent
    if not path.resolve().is_relative_to(root.resolve()):
        raise ValueError(f'Path escapes root: {rel}')
    return path

def denied(rel):
    r = rel.lower().rstrip('/')
    if r.startswith('docs/work/tasks/m-poc'):
        return True
    return any(r == p.lower() or r.startswith(p.lower() + '/') for p in DENIED)

def policy(root):
    return read_json(root / 'docs/work/context-policy.json')['allow']

def permitted(root, rel):
    safe_path(root, rel)
    if denied(rel):
        return False
    return any(rel == p or (p.endswith('/') and rel.startswith(p)) for p in policy(root))

def active_files(root):
    result = set()
    for item in policy(root):
        path = safe_path(root, item)
        if not path.exists():
            continue
        candidates = path.rglob('*') if path.is_dir() else [path]
        for candidate in candidates:
            rel = candidate.relative_to(root).as_posix()
            if candidate.is_file() and '__pycache__' not in candidate.parts and permitted(root, rel):
                result.add(rel)
    return sorted(result)

def card(task):
    lines = [f'# {task["id"]}: {task["title"]}', '',
             '<!-- Generated from docs/work/queue.json; edit the queue, then render. -->', '',
             f'- Status: `{task["status"]}`; kind: `{task["kind"]}`.',
             '- Executor: **GPT-6.1 Sol; reasoning high**. Record actual configuration separately.',
             '- Dependencies: ' + (', '.join(f'[{x}]({x}.md)' for x in task['depends']) or 'None.'),
             f'- Human semantic acceptance required: {str(task["semantic_acceptance_required"]).lower()}.',
             '', '## Goal', '', task['goal']]
    for key,heading in [('outputs','Concrete deliverables'),('start_conditions','Start conditions'),
                        ('inputs','Input contracts'),('context','Required context'),
                        ('write_scope','Allowed write scope'),('exclusions','Exclusions'),
                        ('acceptance','Acceptance criteria'),('tests','Required validation'),
                        ('blockers','Blockers and escalation'),('handoff','Final report and handoff')]:
        lines += ['', '## '+heading, '']
        lines += ['- '+x for x in task[key]] or ['- Use only the task packet and pinned dependency outputs.']
    lines += ['', 'Use [the shared workflow](../WORKFLOW.md) for transitions, review, retries and recovery.',
              'Read only assigned pages/IDs from binary or private inputs; never recursively load a source directory.']
    return '\n'.join(lines)+'\n'

def views(q):
    ready = [t['id'] for t in q['tasks'] if t['status'] == 'ready']
    next_id = ready[0] if ready else None
    rows = ['# WGC roadmap', '', '<!-- Generated from docs/work/queue.json. -->', '',
            '| Task | Status | Kind | Dependencies |', '|---|---|---|---|']
    for t in q['tasks']:
        rows.append(f'| [{t["id"]}: {t["title"]}](work/tasks/{t["id"]}.md) | {t["status"]} | {t["kind"]} | {", ".join(t["depends"]) or "—"} |')
    rows += ['', 'Stages and readiness distinctions: [implementation plan](IG-PLAN.md).',
             'Future `refine` cards must be narrowed before readiness. No product task has been executed by the planning session.']
    blockers = '\n'.join(f'- {b["id"]}: {b["status"]}. {b["reason"]} {b["resolution"]}' for b in q['infrastructure_blockers'])
    status = f'''# WGC status

<!-- Generated from docs/work/queue.json. -->

Queue updated: {q['updated']}. Next ready task: **{next_id or 'none'}**.
Done tasks: {sum(t['status']=='done' for t in q['tasks'])}/{len(q['tasks'])}.
The planning tools do not certify game behavior. Source import, source coverage,
human semantic acceptance, compilation and gameplay readiness are separate gates.

Requested planning configuration: GPT-6 Astra/high. Recorded actual model/reasoning:
{q['session']['actual_model'] or 'unknown'}/{q['session']['actual_reasoning'] or 'unknown'}.
Future executor target: GPT-6.1 Sol/high; verify its actual configuration at claim time.

## Infrastructure blockers

{blockers}

See [handoff](HANDOFF.md), [workflow](work/WORKFLOW.md), [archive register](ARCHIVES.md)
and [environment evidence](work/ENVIRONMENT.md). No inherited commit/push approval exists.
'''
    handoff = f'''# WGC handoff

<!-- Generated from docs/work/queue.json. -->

Next ready task: **{next_id or 'none'}**. Choose one task; do not execute a whole stage.
Read [workflow](work/WORKFLOW.md), then use [operator prompts](work/PROMPTS.md).

```powershell
pwsh -NoProfile -File scripts/check.ps1
.\\.venv\\Scripts\\python.exe scripts/workflow.py next
.\\.venv\\Scripts\\python.exe scripts/workflow.py packet{(' --task '+next_id) if next_id else ''}
```

The packet lists exact context and hashes. It does not launch a model or claim the task.
Use the staged [execution skill](skills/wgc-execute/SKILL.md) explicitly; automatic
installation is pending. Operator selects GPT-6.1 Sol/high, records actual settings,
and follows claim → implementation → independent review → repair → acceptance → done.
Checkpoints and evidence live in private/workflow/runs; preserve prior attempts.

The active SPQR PDF is in private/ig/sources/spqr-5e with verified provenance.
The WGU inspection is input evidence, not a semantic acceptance or an exact current count.
Neighbouring KB/WGU repositories are read-only. Required scenarios/options, missing
materials, authorized semantic reviewer and performance hardware/thresholds must be
pinned in the tasks that need them; they do not prevent the first source-contract task.

External history relocation remains governed by [the archive register](ARCHIVES.md)
and the queue infrastructure blockers. No archive content is needed for this packet.
Do not use old prompts, archived operational approvals or Git history as default context.
'''
    return {'docs/ROADMAP.md':'\n'.join(rows)+'\n', 'docs/STATUS.md':status,
            'docs/HANDOFF.md':handoff, **{f'docs/work/tasks/{t["id"]}.md':card(t) for t in q['tasks']}}

def validate(q, root, check_views=True):
    if q.get('schema_version') != 'wgc-work-1': raise ValueError('Unknown queue format')
    tasks = q['tasks']; ids = [t['id'] for t in tasks]
    if len(ids) != len(set(ids)): raise ValueError('Duplicate task ID')
    by_id = {t['id']:t for t in tasks}
    if sum(t['status'] in BUSY for t in tasks) > 1: raise ValueError('Sequential writer/review ownership conflict')
    visited, visiting = set(), set()
    def visit(id):
        if id in visiting: raise ValueError(f'Dependency cycle at {id}')
        if id in visited: return
        visiting.add(id)
        for dep in by_id[id]['depends']:
            if dep not in by_id: raise ValueError(f'Missing dependency {dep}')
            visit(dep)
        visiting.remove(id); visited.add(id)
    for t in tasks:
        if not re.fullmatch(r'IG-[1-5][A-Z][0-9]*(?:-[A-Z0-9]+)*', t['id']): raise ValueError('Invalid task ID')
        if t['status'] not in TRANSITIONS: raise ValueError('Invalid status')
        if t['kind'] not in {'implementation','content','refine','closure'}: raise ValueError('Invalid kind')
        if t['executor'] != {'model':'GPT-6.1 Sol','model_id':'gpt-6.1-sol','reasoning':'high'}: raise ValueError('Unexpected executor target')
        for field in ('goal','outputs','start_conditions','inputs','write_scope','exclusions','acceptance','tests','blockers','handoff'):
            if not t.get(field) or (isinstance(t[field],list) and not all(isinstance(x,str) and x.strip() for x in t[field])):
                raise ValueError(f'{t["id"]}: missing {field}')
        visit(t['id'])
        for rel in t['context']:
            if not permitted(root, rel): raise ValueError(f'Forbidden context: {rel}')
            if t['status'] != 'planned' and not safe_path(root,rel).is_file(): raise ValueError(f'Missing context: {rel}')
        for rel in t['write_scope']:
            safe_path(root,rel)
            if denied(rel): raise ValueError(f'History in write scope: {rel}')
        if t['status'] in {'ready', *BUSY, 'done'}:
            if t['kind']=='refine': raise ValueError(f'{t["id"]} requires refinement')
            if any(by_id[d]['status']!='done' for d in t['depends']): raise ValueError(f'{t["id"]} has unfinished dependencies')
        if t['status'] in BUSY | {'done','blocked'} and not t['events']:
            raise ValueError('Active/finished/blocked task requires transition evidence')
        previous = None
        for event in t['events']:
            if event['to'] not in TRANSITIONS.get(event['from'],set()) or (previous and previous != event['from']):
                raise ValueError('Invalid event chain')
            previous = event['to']
            p = safe_path(root,event['evidence'])
            if not p.is_file() or digest(p)!=event['sha256']: raise ValueError('Transition evidence changed or missing')
            if 'semantic_decision' in event:
                decision=safe_path(root,event['semantic_decision'])
                if not decision.is_file() or digest(decision)!=event['semantic_sha256']: raise ValueError('Semantic decision changed')
        if previous and previous != t['status']: raise ValueError('Status disagrees with event chain')
    if check_views:
        for rel,body in views(q).items():
            p=root/rel
            if not p.is_file() or p.read_text(encoding='utf-8')!=body: raise ValueError(f'Derived view stale: {rel}; run render')
    return len(tasks)

def packet(q, root, task_id, output=True):
    task = next(t for t in q['tasks'] if t['id']==task_id)
    if task['status'] not in {'ready', *BUSY}: raise ValueError('Task is not ready or active')
    validate(q,root)
    paths = list(dict.fromkeys(BASE_CONTEXT+[f'docs/work/tasks/{task_id}.md']+task['context']))
    files, sections = [], []
    for rel in paths:
        if not permitted(root,rel): raise ValueError(f'Forbidden context: {rel}')
        p=safe_path(root,rel)
        if not p.is_file(): raise ValueError(f'Missing context: {rel}')
        files.append({'path':rel,'bytes':p.stat().st_size,'sha256':digest(p)})
        if p.suffix.lower() in {'.md','.json','.py','.ps1','.toml'}:
            sections.append(f'\n--- FILE: {rel} ---\n'+p.read_text(encoding='utf-8-sig'))
    payload = '\n'.join(sections)
    if len(payload.encode('utf-8'))>100_000: raise ValueError('Packet exceeds 100 KB; narrow exact context instead of truncating')
    result={'format':'wgc-context-1','task':task_id,'queue_sha256':digest(root/QUEUE),
            'files':files,'text_bytes':len(payload.encode('utf-8')),'tokens':None,
            'token_note':'Not measured; bytes are not tokens.','external_inputs':task['inputs']}
    if output:
        out=root/'private/workflow/packets'/f'{task_id}-{uuid.uuid4().hex}'
        out.mkdir(parents=True,exist_ok=False)
        (out/'context.txt').write_text(payload,encoding='utf-8')
        result['context_sha256']=digest(out/'context.txt')
        (out/'manifest.json').write_text(json.dumps(result,indent=2,ensure_ascii=False)+'\n',encoding='utf-8')
        print(out.relative_to(root).as_posix())
    return result

def transition(q,root,task_id,state,evidence):
    t=next(t for t in q['tasks'] if t['id']==task_id)
    old=t['status']
    if state not in TRANSITIONS[old]: raise ValueError(f'Forbidden transition: {old} -> {state}')
    p=safe_path(root,evidence)
    if not evidence.startswith('private/workflow/runs/') or not p.is_file(): raise ValueError('Evidence must be a run artifact')
    e=read_json(p)
    for field in ('role','actor','summary','criteria','artifacts','configuration_evidence'):
        if not e.get(field): raise ValueError(f'Missing evidence field: {field}')
    for a in e['artifacts']:
        ap=safe_path(root,a['path'])
        if denied(a['path']) or not ap.is_file() or digest(ap)!=a['sha256']: raise ValueError('Invalid artifact hash/path')
    if state in {'review','accepted','done'}:
        if not e.get('checks') or any(x.get('exit_code') != 0 or not x.get('command') for x in e['checks']):
            raise ValueError('Passing named checks required')
    expected_role={'in_progress':'executor','review':'executor','accepted':'reviewer','done':'coordinator'}
    if state in expected_role and e['role']!=expected_role[state]: raise ValueError('Wrong transition role')
    if state=='in_progress':
        if e.get('model')!='gpt-6.1-sol' or e.get('reasoning')!='high':
            raise ValueError('Sol/high execution not confirmed; record blocker or explicit owner-approved plan change')
    if state=='accepted':
        delivery=next((x for x in reversed(t['events']) if x['to']=='review'),None)
        if not delivery: raise ValueError('No frozen delivery')
        prior=read_json(root/delivery['evidence'])
        if prior['actor']==e['actor']: raise ValueError('Independent reviewer required')
        if prior['artifacts']!=e['artifacts']: raise ValueError('Review must pin the entire delivery manifest')
        if e.get('criteria')!=t['acceptance']: raise ValueError('Review must account for every acceptance criterion')
        if t['semantic_acceptance_required']:
            decision=safe_path(root,e.get('semantic_decision',''))
            if not e['semantic_decision'].startswith('private/workflow/runs/'):
                raise ValueError('Semantic decision must be preserved with the run')
            d=read_json(decision)
            if d.get('role') not in {'human_owner','human_reviewer'} or not all(d.get(k) for k in ('actor','authorization','targets','basis','decision_artifact')) or d.get('decision')!='accepted':
                raise ValueError('Explicit scoped human semantic decision required')
    if state=='done':
        accepted=next(x for x in reversed(t['events']) if x['to']=='accepted')
        prior=read_json(root/accepted['evidence'])
        if prior['artifacts']!=e['artifacts'] or e['criteria']!=t['acceptance']: raise ValueError('Acceptance delivery/criteria mismatch')
    t['status']=state
    t['events'].append({'from':old,'to':state,'utc':datetime.now(timezone.utc).isoformat(),
                        'evidence':evidence,'sha256':digest(p)})
    if state=='accepted' and t['semantic_acceptance_required']:
        t['events'][-1].update(semantic_decision=e['semantic_decision'],semantic_sha256=digest(decision))
    validate(q,root,check_views=False)

def render(q,root):
    for rel,body in views(q).items():
        p=root/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text(body,encoding='utf-8')

def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('command',choices=['validate','render','next','packet','files','transition','dry-run'])
    parser.add_argument('--task'); parser.add_argument('--to'); parser.add_argument('--evidence')
    args=parser.parse_args(); root=ROOT; q=read_json(root/QUEUE)
    if args.command=='render':
        validate(q,root,check_views=False); render(q,root); print('Rendered task/status views.'); return
    if args.command=='files': print('\n'.join(active_files(root))); return
    validate(q,root)
    ready=[t for t in q['tasks'] if t['status']=='ready']
    if args.command=='validate': print(f'Validated {len(q["tasks"])} tasks, DAG, scope, context and derived views.')
    elif args.command=='next': print(ready[0]['id'] if ready else 'No ready task.')
    elif args.command=='packet': packet(q,root,args.task or ready[0]['id'])
    elif args.command=='dry-run':
        before=digest(root/QUEUE); p=packet(q,root,args.task or ready[0]['id'],output=False)
        assert before==digest(root/QUEUE)
        print(json.dumps({'result':'passed','task':p['task'],'context_files':len(p['files']),
                          'context_bytes':p['text_bytes'],'queue_unchanged':True,
                          'models_launched':0,'product_files_written':0},indent=2))
    elif args.command=='transition':
        if not all((args.task,args.to,args.evidence)): raise ValueError('Specify --task, --to and --evidence')
        lock=root/'private/workflow/queue.lock'; lock.parent.mkdir(parents=True,exist_ok=True)
        # An abandoned lock requires coordinator diagnosis; never steal it automatically.
        fd=os.open(lock,os.O_CREAT|os.O_EXCL|os.O_WRONLY)
        try:
            current=digest(root/QUEUE); q=read_json(root/QUEUE)
            transition(q,root,args.task,args.to,args.evidence)
            if digest(root/QUEUE)!=current: raise ValueError('Queue changed concurrently')
            temp=root/'docs/work/queue.pending.json'
            with temp.open('x',encoding='utf-8') as stream: json.dump(q,stream,ensure_ascii=False,indent=2); stream.write('\n')
            os.replace(temp,root/QUEUE); render(q,root)
            print(f'{args.task} -> {args.to}')
        finally:
            os.close(fd); lock.unlink()

if __name__=='__main__':
    try: main()
    except (ValueError,KeyError,StopIteration,OSError) as error:
        print(f'ERROR: {error}',file=sys.stderr); sys.exit(1)
