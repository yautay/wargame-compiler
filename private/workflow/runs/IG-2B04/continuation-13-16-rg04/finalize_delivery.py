"""Freeze this executor's completed task evidence; never launch another role."""
import hashlib
import json
from pathlib import Path
from datetime import datetime, timezone

ROOT=Path('private/workflow/runs/IG-2B04/continuation-13-16-rg04')
SESSION=Path('private/workflow/orchestrator/20261016T115606Z-694df602/001-IG-2B04-executor-0de1c1e6')

def load(p):return json.loads(Path(p).read_text(encoding='utf-8-sig'))
def write(p,d):Path(p).write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def pin(p):
    p=Path(p)
    return {'path':p.as_posix(),'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size}

def main():
    claim=load(ROOT/'claim.json')
    base={k:v for k,v in claim.items() if k not in ('summary','criteria','artifacts','checks','utc')}
    runtime=load(SESSION/'runtime-configuration.json')
    assert runtime['status']=='confirmed' and runtime['model']=='gpt-6.1-sol' and runtime['reasoning']=='high'
    assert pin(SESSION/'runtime-configuration.json')['sha256']==base['configuration_sha256']
    task=load(SESSION/'task.json')
    test=load(ROOT/'test-report.json')
    assert all(c['exit_code']==0 for c in test['checks'])
    for name in ('preservation-report.json','reference-audit.json','replay-report.json'):
        assert load(ROOT/name)['passed'] is True
    reference=load(ROOT/'reference-audit.json')
    for item in reference['current_reports'].values():assert pin(item['path'])==item
    inventory=load(ROOT/'final-verified/inventory.json')
    coverage=load(ROOT/'coverage-report.json')
    now=datetime.now(timezone.utc)
    measurement={'started_utc':runtime['observed_utc'],'execution_claimed_utc':claim['utc'],
                 'ended_utc':now.isoformat(),
                 'wall_seconds':(now-datetime.fromisoformat(runtime['observed_utc'])).total_seconds(),
                 'wall_time_basis':'Observed CLI startup metadata to delivery freeze.',
                 'input_tokens':None,'output_tokens':None,'operator_seconds':None,
                 'unknown_reason':'Model token usage is not exposed; operator time was not reported.'}
    (ROOT/'delivery-handoff.md').write_text(
        '# IG-2B04 executor delivery\n\n'
        'Fresh physical pages 13-16 inspection and all 113 assigned regions are ready for independent technical review. '
        'The complete 44-page inventory retains every nonassigned record, old link/evidence and registry binding. '
        'Only four assigned placeholder memberships retire; their registry entries remain.\n\n'
        f'The inventory has {len(inventory["regions"])} regions: {coverage["full_44_page"]["denominator_regions"]} denominator regions '
        f'and {coverage["full_44_page"]["context_regions"]} retained context region. This task adds 113 denominator regions and zero context regions. '
        'All assigned transcription remains partial; descriptive/formal semantics remain unprocessed. '
        'No gap or placeholder counts as represented. No semantic acceptance or executable readiness is granted.\n\n'
        'Original renders, proposed-boundary overlays and all regenerated components were visually compared. '
        'The complete markers, diagrams, labels, counters and captions are retained. The page14 Moved-marker boundary was corrected; '
        'note background boundaries and an HI/MI observation label were also corrected. '
        'Both independent replays rebuilt all assigned PDF/PNG/text artifacts from the pinned baseline and registry. '
        'The replay audit compares every byte hash and field, normalizing only output paths and the enclosing inventory revision.\n\n'
        'Validation: all three explicit inventory CLI commands passed; 71 source tests passed; the unchanged repository check passed '
        '242 tests on its final allowed retry; git diff --check passed; preservation/reference/replay audits passed. '
        'Earlier missing-rg failures and the PowerShell setup error remain recorded. The successful check preserved inherited PATH/PYTHONPATH '
        'and appended only the verified supervisor-bound ripgrep directory for legacy test lookup. No repository tests, their assertions, guard or global settings changed.\n\n'
        'The ledger structurally retains the exact current dependency ledger, and continuations retain its exact current continuation report. '
        'The page13 opening anchor and chapter continuation after page16 remain unresolved. Page12 was metadata only; page17 and other targets were not inspected.\n\n'
        'Next action: a fresh independent reviewer must inspect original physical pages13-16, every ledger component, both boundaries, '
        'all frozen hashes, preservation, references, replay comparisons and required checks. Technical acceptance is pending. '
        'Human source-meaning acceptance remains a separate gate. No downstream task was started.\n',encoding='utf-8')
    checks=test['checks']+[
        {'command':'.venv/Scripts/python.exe private/workflow/runs/IG-2B04/continuation-13-16-rg04/audit_delivery.py','exit_code':0,'log':pin(ROOT/'audit-delivery-final.log')},
        {'command':'git diff --check','exit_code':0,'log':pin(ROOT/'diff-check-final.log')}]
    write(ROOT/'checkpoint-delivery.json',{**base,'utc':now.isoformat(),'attempt':ROOT.as_posix(),
        'summary':'Executor work complete; frozen delivery prepared for independent review.',
        'input_packet':pin(SESSION/'packet.json'),'checks':checks,'measurement':measurement,
        'completed_operations':['Fresh original and all component inspection','All assigned evidence regenerated in three trees','Two independent complete replays validated and compared','Full baseline/registry/artifact preservation verified','Source/reference/denominator audits and required checks passed'],
        'blocker':None,'next_operation':'Independent reviewer inspects the frozen delivery and original pages13-16; executor stops after review transition.'})
    manifest=ROOT/'delivery-manifest.json'
    assert not manifest.exists(), 'Delivery envelope must be new'
    # This enumeration is only of this fresh exclusively owned output root, for the
    # explicitly required complete file freeze; it performs no context discovery.
    owned=[pin(p) for p in sorted(ROOT.rglob('*')) if p.is_file() and p!=manifest]
    inputs={}
    for artifact in [*inventory['source'].values()]:
        if isinstance(artifact,dict) and 'path' in artifact:inputs[artifact['path']]=artifact
    for ev in inventory['evidence']:
        for key in ('crop_pdf','text','image'):
            artifact=ev[key]
            if not artifact['path'].startswith(ROOT.as_posix()+'/'):inputs[artifact['path']]=artifact
    contract=load('private/workflow/runs/IG-2B04/rg-recovery-20261016-01/execution-contract.json')
    inputs.update({p['path']:p for p in contract['inputs'].values()})
    for p in (SESSION/'runtime-configuration.json',SESSION/'packet.json',SESSION/'task.json',SESSION/'references.json'):
        inputs[p.as_posix()]=pin(p)
    for item in inputs.values():assert pin(item['path'])==item
    for attempt in test['repository_check']['attempts']:
        for artifact in attempt['artifacts']:inputs[artifact['path']]=artifact
    artifacts=owned+[inputs[k] for k in sorted(inputs)]
    write(manifest,{**base,'utc':now.isoformat(),
        'summary':'Fresh pages13-16 inventory with 113 assigned components, complete independent replays, preserved full44-page baseline and passing checks; independent technical review requested.',
        'criteria':task['acceptance'],
        'criteria_results':[{'criterion':c,'executor_evidence_complete':True,'independent_review_pending':True} for c in task['acceptance']],
        'artifacts':artifacts,'owned_artifact_count':len(owned),'retained_input_artifact_count':len(artifacts)-len(owned),
        'checks':checks,'input_packet':pin(SESSION/'packet.json'),'measurement':measurement,
        'self_discovered_candidate_defects':{'medium':1,'low':3,'resolved':['Moved marker top boundary','Two design-note background starts','HI/MI observation label']},
        'unmet_criteria':['Fresh independent technical review of the frozen complete delivery and original assigned pages is pending.'],
        'semantic_acceptance_granted':False,'executable_readiness':'unverified',
        'freeze_note':'This envelope is frozen by the queue transition hash. Every owned file existing before this envelope, all retained source evidence and selected validation logs are pinned; the envelope cannot recursively hash itself.',
        'next_operation':'Supervisor starts the independent reviewer; this executor stops after transition to review.'})
    print(json.dumps({'delivery':pin(manifest),'artifacts':len(artifacts),'owned_artifacts':len(owned)}))

if __name__=='__main__':main()
