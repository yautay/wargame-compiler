"""Audit existing inputs and display source/output for manual review, never infer."""
from pathlib import Path
from datetime import datetime,timezone
import json,hashlib,sys
ROOT=Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';M=Path(__file__).resolve().parent
R=P/'reviews/semantic-01'
def load(p):return json.loads(p.read_bytes())
def ref(p):
    b=p.read_bytes();return dict(path=p.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(p,x):
    assert not p.exists(),p
    p.write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
mode=sys.argv[1]
if mode=='start':
    protected=[ref(f) for f in sorted(P.rglob('*')) if f.is_file() and M not in f.parents and f!=P/'measurement/sessions.jsonl']
    state=load(R/'current-state-11.json');C=load(R/'checklist.json')
    for a in [C['source'],C['evaluation'],*C['responses'].values()]:assert ref(ROOT/a['path'])==a
    save(M/'start.json',dict(card='M-POC5A.4b2',recorded_at_utc=datetime.now(timezone.utc).isoformat(),protected=protected,
        sessions_before=ref(P/'measurement/sessions.jsonl'),prior_state=ref(R/'current-state-11.json'),
        estimate_before_semantic_review=dict(minutes_range=[60,75],assigned_ids=30,occurrences=60,shared_source_separate_original_answers=True,further_split_required=False),
        original_inputs_verified=[C['source'],C['evaluation'],*C['responses'].values()],instruction_is_semantic_acceptance=False,
        model_selector='unknown',reasoning_selector='unknown',active_time='unknown'))
    print('Start/estimate recorded; protected',len(protected))
elif mode=='required':
    entries=[]
    for run in ['first-001','context-01']:
        entries += [P/f'runs/{run}/{f}' for f in ['run.json','session-evidence.txt']]
        entries += [P/f'proposals/{run}/{f}' for f in ['proposal.json','provenance.json']]
        entries += [P/f'reports/{run}/{f}' for f in ['report.md','errors.json','inventory.json','metrics.json','dependency-comparison.json','manifest.json','closure.json']]
    entries += [P/s for s in ['reports/context-01/context-comparison.json','measurement/M-POC4B-context-01/report-reference-supplement.json',
        'reviews/context-source-01/decision-01.json','reviews/context-source-01/review-closure-01.json','source/source-v1.json','inputs/v1/manifest.json',
        'context/pass-01/manifest.json','context/pass-01/freeze-v1.json','transfer/context-v1/context/pass-01/manifest.json',
        'measurement/M-POC5A-part04b-preparation-001/scope-plan.json','inputs/v1/helper-regions.json','context/pass-01/evidence/8.46-step-4-helper.txt']]
    entries += [P/'evaluation/eval-v1'/f for f in ['expectations.json','inventory.json','dependencies.json','measurement-policy.json','manifest.json']]
    entries += [R/f for f in ['checklist.json','review.md','issues.json','current-state-11.json','owner-decision-05.json','owner-review-overlay-05.json','owner-review-summary-05.md']]
    entries += [ROOT/f for f in ['CLAUDE.md','docs/SESSION-PLAYBOOK.md','docs/STATUS.md','docs/HANDOFF.md','docs/handoff/2026-10-11-M-POC5A-owner-review-05.md',
        'docs/ROADMAP.md','docs/POC-PLAN.md','docs/adr/ADR-0039-archiwum-i-poc-przed-architektura.md','docs/work/tasks/M-POC5A.md',
        'docs/work/tasks/semantic/M-POC5A.4.md','docs/work/tasks/semantic/M-POC5A.4b.md','docs/work/tasks/semantic/M-POC5A.4b2.md']]
    for p in entries:
        b=p.read_bytes();x=json.loads(b) if p.suffix=='.json' else b.decode('utf-8-sig')
        print(p.relative_to(ROOT).as_posix(),len(b),'parsed' if isinstance(x,(list,dict)) else 'read')
    save(M/'read-inputs.json',dict(files=[ref(p) for p in entries],method='Entire bytes read/JSON parsed; source-specific manual comparison and visual checks separately recorded. Not semantic certification.'))
elif mode=='edges':
    ids=load(P/'measurement/M-POC5A-part04b-preparation-001/scope-plan.json')['parts'][1]['output_edge_ids'][int(sys.argv[2]):int(sys.argv[3])]
    props={run:load(P/f'proposals/{run}/proposal.json') for run in ['first-001','context-01']}
    for eid in ids:
        print('\nEDGE',eid)
        vals={run:next(x for x in prop['dependencies'] if x['id']==eid) for run,prop in props.items()}
        print('identical_edges',vals['first-001']==vals['context-01'])
        for run,e in vals.items():
            if run=='context-01' and vals['first-001']==e:continue
            print(run,json.dumps(e,ensure_ascii=False))
        for endpoint in dict.fromkeys(x['from'] for x in vals.values()):
            print('SOURCE',endpoint)
            prev=None
            for run,prop in props.items():
                rec=next(x for x in prop['rules']+prop['nodes'] if x['id']==endpoint)
                out={k:(v.get('value',v) if isinstance(v,dict) else v) for k,v in rec.items() if k in ['content','transcription','conditions','action_effect','exceptions','gap_ids']}
                if prev==out:continue
                print(run,json.dumps(out,ensure_ascii=False));prev=out
elif mode=='source':
    regions=load(P/'inputs/v1/helper-regions.json')['regions']
    for region in sys.argv[2:]:
        x=next(x for x in regions if x['region_id']==region);print('\nREGION',region,'\n'+x['text'])
elif mode=='inventory':
    for x in load(P/'evaluation/eval-v1/inventory.json')['items']:
        if x['id'] in sys.argv[2:]:print(x['id'],json.dumps(x,ensure_ascii=False))
