"""Deterministic reading/audit helper; no inference or answer mutation."""
from pathlib import Path
from datetime import datetime, timezone
import json, hashlib, sys
ROOT=Path(__file__).resolve().parents[5]
P=ROOT/'private/poc/spqr-chapter9'
M=Path(__file__).resolve().parent
sys.stdout.reconfigure(encoding='utf-8')
def load(p): return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes()
    return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,o):
    assert not p.exists(),p
    p.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
C=load(P/'reviews/semantic-01/checklist.json')
mode=sys.argv[1]
if mode=='start':
    protected=[]
    for tree in ['source','runs','proposals','reports','inputs','context','transfer','evaluation','reviews','measurement']:
        protected.extend(ref(f) for f in sorted((P/tree).rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl')
    save(M/'start.json',dict(card='M-POC5A',part='M-POC5A.4a',recorded_at_utc=datetime.now(timezone.utc).isoformat(),bootstrap_start='unknown',protected=protected,sessions_before=ref(P/'measurement/sessions.jsonl'),instruction_is_acceptance=False,model_selector='unknown',reasoning_selector='unknown'))
    print('Protected:',len(protected))
elif mode=='structure':
    for rel in ['runs/first-001/run.json','runs/context-01/run.json','proposals/first-001/provenance.json','proposals/context-01/provenance.json','evaluation/eval-v1/expectations.json','evaluation/eval-v1/inventory.json','evaluation/eval-v1/dependencies.json','reviews/semantic-01/owner-decision-01.json','reviews/semantic-01/owner-decision-02.json','reviews/semantic-01/owner-review-overlay-02.json']:
        o=load(P/rel); print(rel,ref(P/rel),{k:(len(v) if isinstance(v,(list,dict)) else v) for k,v in o.items()})
elif mode=='exp':
    lo,hi=map(int,sys.argv[2:4])
    for e in C['expectations'][lo-1:hi]:
        print(json.dumps({k:e[k] for k in ['id','classification','criticality','source_scope','inventory_refs','limits','exclusions']},ensure_ascii=False))
        print('SOURCE',json.dumps([dict(id=v.get('inventory_ref'),page=v['pdf_page'],column=v.get('column'),span=v.get('source_span',v.get('transcription')),envelope=v.get('transcription') if 'source_span' in v else None) for v in e['source_evidence']],ensure_ascii=False))
        print('RUN MAPPING',json.dumps({r:dict(ids=v['output_record_ids'],gaps=[g['id'] for g in v['extractor_gap_claims']]) for r,v in e['runs'].items()},ensure_ascii=False))
elif mode=='records':
    ids=sys.argv[2:]
    for rid in ids:
        a=C['output_records']['first-001'].get(rid); b=C['output_records']['context-01'].get(rid)
        print('\nRECORD',rid,'same_values',a and b and a['original_record']==b['original_record'])
        for run,t in [('first-001',a),('context-01',b)]:
            if not t: continue
            if run=='context-01' and a and a['original_record']==b['original_record']: print(run,t['pointer'],t['raw_span']); continue
            print(run,t['pointer'],t['raw_span'],json.dumps(t['original_record'],ensure_ascii=False))
elif mode=='issues':
    for rel in ['reviews/semantic-01/issues.json','reviews/semantic-01/part-02/issues.json','reviews/semantic-01/part-03/issues.json']:
        o=load(P/rel)
        for i in o['issues']: print(rel,json.dumps({k:v for k,v in i.items() if k not in ['output_trace','source_evidence','evidence','responses','response_refs','evaluation_manifest','source_scope','evaluation']},ensure_ascii=False))
elif mode=='required':
    rels=[]
    for run in ['first-001','context-01']:
        rels.extend([f'runs/{run}/run.json',f'runs/{run}/session-evidence.txt',f'proposals/{run}/proposal.json',f'proposals/{run}/provenance.json'])
        rels.extend(f'reports/{run}/{f}' for f in ['report.md','errors.json','inventory.json','metrics.json','dependency-comparison.json','manifest.json','closure.json'])
    rels.extend(['reports/context-01/context-comparison.json','measurement/M-POC4B-context-01/report-reference-supplement.json','reviews/context-source-01/decision-01.json','reviews/context-source-01/review-closure-01.json','source/source-v1.json','inputs/v1/manifest.json','context/pass-01/manifest.json','context/pass-01/freeze-v1.json','transfer/context-v1/context/pass-01/manifest.json'])
    rels.extend('evaluation/eval-v1/'+f for f in ['expectations.json','inventory.json','dependencies.json','measurement-policy.json','manifest.json'])
    rels.extend('reviews/semantic-01/'+f for f in ['checklist.json','review.md','issues.json','current-state-05.json','owner-decision-01.json','owner-decision-02.json','owner-review-overlay-02.json','owner-review-summary-02.md'])
    for part in ['part-02','part-03']: rels.extend(f.relative_to(P).as_posix() for f in sorted((P/'reviews/semantic-01'/part).iterdir()) if f.is_file())
    read=[]
    for rel in rels:
        f=P/rel; b=f.read_bytes(); o=load(f) if f.suffix=='.json' else b.decode('utf-8-sig')
        read.append(ref(f))
        if f.suffix=='.json':
            if rel.endswith('run.json'): print(rel,json.dumps({k:o[k] for k in ['extraction_configuration','timing','session_evidence','assessment','documentation_gaps'] if k in o},ensure_ascii=False))
            elif rel.endswith(('manifest.json','freeze-v1.json','closure.json')): print(rel,{k:(len(v) if isinstance(v,(list,dict)) else v) for k,v in o.items()})
            elif rel.endswith(('metrics.json','context-comparison.json','measurement-policy.json')):
                print(rel,json.dumps({k:v for k,v in o.items() if not isinstance(v,list) and k not in ['rules','relationships','categories','runs','situations','group_results']},ensure_ascii=False))
    save(M/'read-inputs.json',dict(files=read,method='Full bytes read and JSON parsed; evaluator separately inspected relevant original records, source spans, graphics and closed reports. Reading/parse alone does not establish meaning.',required_files=len(read)))
    print('READ',len(read))
