"""Read/audit original evidence only; no inference or response mutations."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'; M=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def load(p): return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes(); return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mode=sys.argv[1]
if mode=='start':
    protected=[ref(f) for tree in ['source','runs','proposals','reports','inputs','context','transfer','evaluation','reviews','measurement','prompts'] for f in sorted((P/tree).rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
    save(M/'start.json',dict(card='M-POC5A.4b1',recorded_at_utc=datetime.now(timezone.utc).isoformat(),bootstrap_start='unknown',protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),estimate_before_semantic_review=dict(minutes_range=[75,90],assigned_ids=65,occurrences=125,extra_frozen_tuples=22,method='Shared supplied source scopes, separately traced answers; all assigned IDs plus frozen tuple comparisons, no further split required. Calendar time is not active time/budget compliance.'),instruction_is_acceptance=False,model_selector='unknown',reasoning_selector='unknown'))
    print('Protected:',len(protected))
elif mode=='required':
    rels=[]
    for run in ['first-001','context-01']:
        rels += [f'runs/{run}/{f}' for f in ['run.json','session-evidence.txt']]
        rels += [f'proposals/{run}/{f}' for f in ['proposal.json','provenance.json']]
        rels += [f'reports/{run}/{f}' for f in ['report.md','errors.json','inventory.json','metrics.json','dependency-comparison.json','manifest.json','closure.json']]
    rels += ['reports/context-01/context-comparison.json','measurement/M-POC4B-context-01/report-reference-supplement.json','reviews/context-source-01/decision-01.json','reviews/context-source-01/review-closure-01.json','source/source-v1.json','inputs/v1/manifest.json','context/pass-01/manifest.json','context/pass-01/freeze-v1.json','transfer/context-v1/context/pass-01/manifest.json','measurement/M-POC5A-part04b-preparation-001/scope-plan.json']
    rels += ['evaluation/eval-v1/'+f for f in ['expectations.json','inventory.json','dependencies.json','measurement-policy.json','manifest.json']]
    rels += ['reviews/semantic-01/'+f for f in ['checklist.json','review.md','issues.json','current-state-07.json','current-state-08.json','owner-decision-01.json','owner-decision-02.json','owner-decision-03.json','owner-review-overlay-03.json','owner-review-summary-03.md']]
    for part in ['part-02','part-03','part-04a']:
        rels += [f.relative_to(P).as_posix() for f in sorted((P/'reviews/semantic-01'/part).iterdir()) if f.is_file()]
    for r in rels:
        f=P/r; b=f.read_bytes(); o=load(f) if f.suffix=='.json' else b.decode('utf-8-sig')
        print(r,ref(f)['sha256'], [(k,len(v) if isinstance(v,(list,dict)) else str(v)[:130]) for k,v in o.items()] if isinstance(o,dict) else o)
    save(M/'read-inputs.json',dict(files=[ref(P/r) for r in rels],method='Entire bytes read/JSON parsed. Separate selective source, output and policy inspection required and recorded in review; parse does not certify meaning.',required_files=len(rels)))
elif mode=='edges':
    plan=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json')
    ids=plan['parts'][0]['output_edge_ids'][int(sys.argv[2]):int(sys.argv[3])]
    props={r:load(P/f'proposals/{r}/proposal.json') for r in ['first-001','context-01']}
    for eid in ids:
        print('\nEDGE',eid)
        a=next((e for e in props['first-001']['dependencies'] if e['id']==eid),None)
        b=next((e for e in props['context-01']['dependencies'] if e['id']==eid),None)
        print('same',a==b)
        for r,e in [('first-001',a),('context-01',b)]:
            if r=='context-01' and a==b: continue
            print(r,json.dumps(e,ensure_ascii=False))
elif mode=='frozen':
    d=load(P/'evaluation/eval-v1/dependencies.json')
    for k in ['counts','metric_denominators','confirmed_execution_relations','mentions','continuations']:
        print(k,json.dumps(d[k],ensure_ascii=False))
elif mode=='records':
    c=load(P/'reviews/semantic-01/checklist.json')
    for rid in sys.argv[2:]:
        print('\nRECORD',rid)
        a=c['output_records']['first-001'].get(rid); b=c['output_records']['context-01'].get(rid)
        for r,t in [('first-001',a),('context-01',b)]:
            if r=='context-01' and a==b: continue
            print(r,json.dumps(t,ensure_ascii=False))
elif mode=='endpoints':
    plan=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json')
    ids=plan['parts'][0]['output_edge_ids'][int(sys.argv[2]):int(sys.argv[3])]
    props={r:load(P/f'proposals/{r}/proposal.json') for r in ['first-001','context-01']}
    endpoints=set()
    for r,d in props.items():
        for e in d['dependencies']:
            if e['id'] in ids: endpoints.update(x for x in [e['from'],e['to']] if x)
    prev={}
    for r,d in props.items():
        for e in d['nodes']+d['rules']:
            if e['id'] not in endpoints: continue
            q={k:v.get('value',v) if isinstance(v,dict) else v for k,v in e.items() if k in ['content','transcription','conditions','action_effect','exceptions','gap_ids']}
            if prev.get(e['id'])==q: continue
            print(r,e['id'],json.dumps(q,ensure_ascii=False));prev[e['id']]=q
