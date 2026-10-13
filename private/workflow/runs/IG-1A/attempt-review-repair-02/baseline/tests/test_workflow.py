"""Behavioral checks for planning controls; never read historical payloads."""
import copy
import importlib.util
import json
from pathlib import Path
import re
import subprocess
from urllib.parse import unquote

import pytest

ROOT = Path(__file__).resolve().parents[1]
spec=importlib.util.spec_from_file_location('workflow', ROOT/'scripts/workflow.py')
w=importlib.util.module_from_spec(spec)
spec.loader.exec_module(w)

def dump(path,obj):
    path.parent.mkdir(parents=True,exist_ok=True)
    path.write_text(json.dumps(obj,indent=2),encoding='utf-8')

@pytest.fixture
def sandbox(tmp_path):
    q=w.read_json(ROOT/w.QUEUE)
    # Only the source-contract task; no real source or archived data in the fixture.
    q['tasks']=copy.deepcopy(q['tasks'][:1])
    # The synthetic state-machine tests always start before the first claim.
    q['tasks'][0]['status']='ready'
    q['tasks'][0]['events']=[]
    for rel in w.BASE_CONTEXT + q['tasks'][0]['context']:
        p=tmp_path/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_text('Synthetic context\n',encoding='utf-8')
    dump(tmp_path/'docs/work/context-policy.json',w.read_json(ROOT/'docs/work/context-policy.json'))
    dump(tmp_path/w.QUEUE,q); w.render(q,tmp_path)
    return tmp_path,q

def evidence(root,q,name,role='executor',actor='executor-1'):
    artifact=root/'tests/contracts/synthetic.txt'; artifact.parent.mkdir(parents=True,exist_ok=True)
    if not artifact.exists(): artifact.write_text('Synthetic deliverable',encoding='utf-8')
    rel=f'private/workflow/runs/IG-1A/attempt-1/{name}.json'
    body={'role':role,'actor':actor,'summary':name,'model':'gpt-6.1-sol','reasoning':'high',
          'configuration_evidence':'Synthetic test observation, not actual execution',
          'criteria':q['tasks'][0]['acceptance'],
          'checks':[{'command':'synthetic check','exit_code':0}],
          'artifacts':[{'path':'tests/contracts/synthetic.txt','sha256':w.digest(artifact)}]}
    dump(root/rel,body)
    return rel

def test_current_plan_and_derived_views():
    assert w.validate(w.read_json(ROOT/w.QUEUE),ROOT) >= 30

def test_next_packet_does_not_need_history(sandbox):
    root,q=sandbox
    # The test workspace has no archives at all.
    before=(root/w.QUEUE).read_bytes()
    p=w.packet(q,root,'IG-1A',output=False)
    assert p['files'] and p['text_bytes']>0
    assert all(not w.denied(f['path']) for f in p['files'])
    assert before==(root/w.QUEUE).read_bytes()

@pytest.mark.parametrize('path',['archive/poc/secrets.md','private/archive/a.md','.git/config','docs/work/tasks/IG-0.md','docs/work/tasks/M-POC5A.md','docs/work/tasks/README.md','docs/POC-PLAN.md','../outside.md','docs/../../outside.md','C:/outside.md'])
def test_history_and_path_escape_are_rejected(sandbox,path):
    root,q=sandbox; q['tasks'][0]['context'].append(path)
    with pytest.raises(ValueError): w.validate(q,root,False)

def test_cycle_and_missing_dependency_are_rejected(sandbox):
    root,q=sandbox; q['tasks'][0]['depends']=['IG-1A']
    with pytest.raises(ValueError,match='cycle'): w.validate(q,root,False)
    q['tasks'][0]['depends']=['IG-9Z']
    with pytest.raises(ValueError,match='Missing dependency'): w.validate(q,root,False)

def test_missing_acceptance_and_unrefined_ready_are_rejected(sandbox):
    root,q=sandbox; original=q['tasks'][0]['acceptance']; q['tasks'][0]['acceptance']=[]
    with pytest.raises(ValueError,match='acceptance'): w.validate(q,root,False)
    q['tasks'][0]['acceptance']=original; q['tasks'][0]['kind']='refine'
    with pytest.raises(ValueError,match='refinement'): w.validate(q,root,False)

def test_full_sequential_dry_run_and_review_independence(sandbox):
    root,q=sandbox
    for state,name,role,actor in [('in_progress','claim','executor','worker'),('review','delivery','executor','worker')]:
        w.transition(q,root,'IG-1A',state,evidence(root,q,name,role,actor))
    with pytest.raises(ValueError,match='Independent reviewer'):
        w.transition(q,root,'IG-1A','accepted',evidence(root,q,'self-review','reviewer','worker'))
    w.transition(q,root,'IG-1A','accepted',evidence(root,q,'review','reviewer','reviewer-2'))
    w.transition(q,root,'IG-1A','done',evidence(root,q,'accept','coordinator','coordinator'))
    w.render(q,root); w.validate(q,root)
    assert q['tasks'][0]['status']=='done'
    assert [e['to'] for e in q['tasks'][0]['events']]==['in_progress','review','accepted','done']

def test_cannot_skip_review_or_forge_done(sandbox):
    root,q=sandbox
    with pytest.raises(ValueError,match='Forbidden transition'):
        w.transition(q,root,'IG-1A','done',evidence(root,q,'bad','coordinator'))
    q['tasks'][0]['status']='done'
    with pytest.raises(ValueError,match='requires transition evidence'): w.validate(q,root,False)

def test_delivered_bytes_and_evidence_cannot_change(sandbox):
    root,q=sandbox
    w.transition(q,root,'IG-1A','in_progress',evidence(root,q,'claim'))
    delivery=evidence(root,q,'delivery'); w.transition(q,root,'IG-1A','review',delivery)
    (root/'tests/contracts/synthetic.txt').write_text('Changed after freeze',encoding='utf-8')
    # A new review manifest cannot replace the exact frozen delivery.
    with pytest.raises(ValueError,match='entire delivery'):
        w.transition(q,root,'IG-1A','accepted',evidence(root,q,'review','reviewer','independent'))
    (root/delivery).write_text('{}',encoding='utf-8')
    with pytest.raises(ValueError,match='evidence changed'): w.validate(q,root,False)

def test_unknown_configuration_cannot_claim_target(sandbox):
    root,q=sandbox; p=evidence(root,q,'claim'); e=w.read_json(root/p); e['model']=None; dump(root/p,e)
    with pytest.raises(ValueError,match='not confirmed'): w.transition(q,root,'IG-1A','in_progress',p)

def test_semantics_requires_human_decision(sandbox):
    root,q=sandbox; q['tasks'][0]['semantic_acceptance_required']=True
    w.transition(q,root,'IG-1A','in_progress',evidence(root,q,'claim'))
    w.transition(q,root,'IG-1A','review',evidence(root,q,'delivery'))
    with pytest.raises(ValueError): w.transition(q,root,'IG-1A','accepted',evidence(root,q,'review','reviewer','independent'))

def test_block_and_resume_require_replanning(sandbox):
    root,q=sandbox
    w.transition(q,root,'IG-1A','blocked',evidence(root,q,'block','coordinator'))
    with pytest.raises(ValueError,match='Forbidden transition'):
        w.transition(q,root,'IG-1A','in_progress',evidence(root,q,'invalid-resume'))
    w.transition(q,root,'IG-1A','planned',evidence(root,q,'resolve','coordinator'))
    w.transition(q,root,'IG-1A','ready',evidence(root,q,'ready','coordinator'))
    assert q['tasks'][0]['status']=='ready'

def test_active_markdown_links():
    for rel in w.active_files(ROOT):
        if not rel.endswith('.md'): continue
        path=ROOT/rel
        body=re.sub(r'^```.*?^```\s*$','',path.read_text(encoding='utf-8'),flags=re.M|re.S)
        for href in re.findall(r'\[[^\]]*\]\(([^)\s]+)\)',body):
            if re.match(r'^[a-zA-Z][a-zA-Z0-9+.-]*:',href): continue
            target,_,anchor=unquote(href).partition('#')
            dest=(path.parent/target).resolve() if target else path
            assert dest.exists(),f'{rel}: {href}'
            assert not w.denied(dest.relative_to(ROOT).as_posix()),f'Active navigation to history: {rel}: {href}'
            if anchor:
                headings=re.findall(r'^#{1,6}\s+(.+)$',dest.read_text(encoding='utf-8'),re.M)
                slugs={re.sub(r'[^\w -]','',h.lower()).replace(' ','-') for h in headings}
                assert anchor in slugs

def test_default_ripgrep_excludes_history():
    result=subprocess.run(['rg','--files'],cwd=ROOT,capture_output=True,text=True,check=True)
    paths=[x.replace('\\','/') for x in result.stdout.splitlines()]
    assert paths and not any(w.denied(p) or p.startswith('private/') for p in paths)

def test_skill_frontmatter_and_no_placeholder():
    for p in (ROOT/'docs/skills').glob('*/SKILL.md'):
        body=p.read_text(encoding='utf-8')
        front=body.split('---',2)[1]
        assert re.search(r'^name: '+p.parent.name+'$',front,re.M)
        assert re.search(r'^description: .{30,}$',front,re.M)
        assert 'TODO' not in body and 'TBD' not in body
