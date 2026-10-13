"""Check cumulative scope, original bytes and the concrete new-session handoff."""
from pathlib import Path
from collections import Counter
import hashlib
import json
import sys

sys.stdout.reconfigure(encoding='utf-8')
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
REV=P/'reviews/semantic-01'
def load(path):return json.loads(path.read_bytes())
def ref(path):
    b=path.read_bytes();return dict(path=path.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def resolve(obj,pointer):
    for k in pointer.lstrip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');obj=obj[int(k)] if isinstance(obj,list) else obj[k]
    return obj

start=load(M/'start.json')
for r in start['protected']:assert ref(ROOT/r['path'])==r,r['path']
decision=load(REV/'owner-decision-02.json');overlay=load(REV/'owner-review-overlay-02.json')
C=load(REV/'checklist.json');D=load(REV/'part-03/comparisons.json')
expected={f'EXP-{n:03}' for n in list(range(26,31))+[32]+list(range(34,40))+list(range(41,50))}
assert decision['owner_reply']=='Akceptuję i podaj prompt dla nowej sesji'
assert {r['id'] for r in decision['scopes']}==expected|{'EXP-031','EXP-033'}
assert len(decision['scopes'])==23 and decision['M_POC5A_closed'] is False
assert decision['context_acceptance_is_gap_closure'] is False
for r in list(C['responses'].values())+[C['evaluation'],C['source']]:assert ref(ROOT/r['path'])==r
for scope in decision['scopes']:
    e=next(x for x in D['expectations'] if x['id']==scope['id'])
    assert scope['reviewed_scope']==e['source_scope'] and scope['source_evidence']==e['source_evidence']
    assert scope['status']=='reviewed' and scope['reviewer']==decision['reviewer']
    assert scope['whole_record_accepted'] is False
    if scope['classification']=='requires_context':
        assert scope['result']=='correct_source_requirement_declaration' and scope['full_dependent_result']=='blocked_source'
    else:assert scope['result']=='correct_in_owner_accepted_scope'
    for run,trace in scope['output_trace'].items():
        raw=(ROOT/C['responses'][run]['path']).read_bytes();obj=json.loads(raw)
        for rid,t in trace.items():
            assert t['pointer']==e['runs'][run]['output_trace'][rid]['pointer']
            s=t['raw_span'];piece=raw[s['start_byte']:s['end_byte_exclusive']]
            assert hashlib.sha256(piece).hexdigest()==s['sha256'] and json.loads(piece)==resolve(obj,t['pointer'])
for run,r in overlay['runs'].items():
    assert len(r['scopes'])==43 and len({s['id'] for s in r['scopes']})==43
    assert len(r['context_requirements'])==2
    assert r['accepted_scoped_groups']==43 and r['pending_content_groups']==23
    assert r['reviewed_context_groups']==2 and r['pending_context_groups']==6
    assert all(s['response']==C['responses'][run] for s in r['scopes']+r['context_requirements'])
    assert all(s['full_dependent_result']=='blocked_source' for s in r['context_requirements'])
    assert r['complete_rule_quality']=='not_assessable' and r['semantic_TP_FP_FN']=='not_assessable'
assert len(overlay['category_units'])==175 and len({r['id'] for r in overlay['category_units']})==175
assert Counter(r['category'] for r in overlay['category_units'])==overlay['category_accepted_scope_counts']
assert overlay['category_full_denominators']==C['counts']['categories']
assert len(overlay['pending_expectation_ids'])==29
assert set(overlay['pending_expectation_ids'])=={f'EXP-{n:03}' for n in [10,17,19,40,50]+list(range(51,75))}
assert overlay['all_output_edges_review']=='pending' and overlay['all_locator_review']=='unchanged'
current=load(REV/'current-state-05.json')
assert current['decision']==ref(REV/'owner-decision-02.json')
assert current['overlay']==ref(REV/'owner-review-overlay-02.json') and current['next_part']=='M-POC5A.4a'
assert current['remaining_uncompared_expectations']==24 and current['M_POC5A_closed'] is False
for r in load(M/'decision-artifacts.json')['artifacts']:assert ref(ROOT/r['path'])==r
assert ref(P/'measurement/sessions.jsonl')==start['sessions_before']
prompt=P/'prompts/semantic-review-part04a-start-v1.txt'
body=prompt.read_text(encoding='utf-8')
for s in ['C:\\repo\\wargame-compiler','feature/tests','current-state-05.json','owner-decision-02.json',
          'EXP-051–074','43/66','2/8','29 oczekiwań','M-POC5A.4a','scripts/check.ps1','git diff --check']:
    assert s in body,s
for r in C['responses'].values():assert r['sha256'] in body
assert C['evaluation']['sha256'] in body
assert 'Nie uruchamiaj\n.4b/.4c/.4d w tej samej sesji' in body
assert (ROOT/'docs/handoff/2026-10-10-M-POC5A-owner-review-02.md').exists()
for n in 'abcd':
    card=ROOT/f'docs/work/tasks/semantic/M-POC5A.4{n}.md'
    assert card.exists() and f'**ID:** M-POC5A.4{n}' in card.read_text(encoding='utf-8')
result=dict(result='passed',new_local_scopes=21,new_context_requirement_scopes=2,
    local_groups_per_answer=43,reviewed_context_groups_per_answer=2,pending_expectations=29,
    category_units=175,protected_files=len(start['protected']),source_requirements_still_block_full_results=True,
    previous_measurements_unchanged=True,new_session_part='M-POC5A.4a',prompt=ref(prompt),whole_card='partial')
target=M/'validation.json';assert not target.exists();target.write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,ensure_ascii=False))
