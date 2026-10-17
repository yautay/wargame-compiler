import hashlib
import importlib.util
import json
from pathlib import Path

base = Path('private/workflow/runs/IG-2B03/preparation-003-e285fb76')
def load(p):
    return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def sha(p):
    return hashlib.sha256(Path(p).read_bytes()).hexdigest()
q = load('docs/work/queue.json')
old = load(base/'queue-before.json')
selected = next(t for t in q['tasks'] if t['id']=='IG-2B03')
previous = next(t for t in old['tasks'] if t['id']=='IG-2B03')
for before, after in zip(old['tasks'], q['tasks']):
    if before['id'] != 'IG-2B03':
        assert before == after, before['id']
assert len(old['tasks']) == len(q['tasks'])
assert {k:v for k,v in old.items() if k!='tasks'} == {k:v for k,v in q.items() if k!='tasks'}
assert selected['acceptance'][:len(previous['acceptance'])] == previous['acceptance']
assert selected['tests'][:len(previous['tests'])] == previous['tests']
assert selected['semantic_acceptance_required'] == previous['semantic_acceptance_required']
assert selected['depends'] == previous['depends']
assert all(next(t for t in q['tasks'] if t['id']==d)['status']=='done' for d in selected['depends'])
inputs = load(base/'input-pins.json')
for item in inputs['files'] + inputs['context_only_evidence']:
    assert sha(item['path']) == item['sha256'], item['path']
scope = load(base/'scope.json')
assert scope['assigned_physical_pages'] == [9,10,11,12]
assert selected['target_ids'] == [p['id'] for p in inputs['assigned_page_records']]
assert len(set(selected['target_ids'])) == 4
assert set(selected['target_ids']).isdisjoint(selected['context_only_ids'])
assert selected['context_only_ids'] == scope['context_only_ids'] == inputs['context_only_ids']
assert not Path(scope['output_root']).exists(), 'Coordinator must not write executor products'
spec=importlib.util.spec_from_file_location('workflow', 'scripts/workflow.py')
w=importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)
w.validate(q, Path.cwd())
paths=list(dict.fromkeys(w.BASE_CONTEXT+['docs/work/tasks/IG-2B03.md']+selected['context']))
sections=[]
for rel in paths:
    assert w.permitted(Path.cwd(),rel) and Path(rel).is_file(),rel
    if Path(rel).suffix.lower() in {'.md','.json','.py','.ps1','.toml'}:
        sections.append('\n--- FILE: '+rel+' ---\n'+Path(rel).read_text(encoding='utf-8-sig'))
context_bytes=len('\n'.join(sections).encode('utf-8'))
assert context_bytes <= 100_000
oldpolicy=load(base/'context-policy-before.json')
policy=load('docs/work/context-policy.json')
assert policy['allow'][:len(oldpolicy['allow'])] == oldpolicy['allow']
inspection=load(base/'source-inspection.json')
assert inspection['visual_inspection_completed'] and inspection['assigned_pages']==[9,10,11,12]
for artifact in inspection['renders']:
    assert sha(artifact['path'])==artifact['sha256']
assert inspection['configuration_evidence']==scope['configuration_evidence']
assert sha(scope['configuration_evidence'])==scope['configuration_sha256']
print(json.dumps(dict(result='pass', task='IG-2B03', other_tasks_unchanged=True, original_acceptance_and_tests_preserved=True, complete_context_available=True, context_bytes=context_bytes, dependencies_done=True, input_pins_verified=True, assigned_pages=[9,10,11,12], executor_products_written=False, semantic_acceptance_granted=False)))
