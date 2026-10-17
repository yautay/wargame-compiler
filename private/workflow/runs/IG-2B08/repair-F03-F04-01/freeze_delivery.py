"""Freeze the current F03/F04 repair after actual complete validation."""
from datetime import datetime, timezone
from pathlib import Path
from build_inventory import ROOT, SESSION, TASK, SPECS, load, write, pin, metadata, old_preservation


def main():
    meta = metadata()
    assert meta['configuration_sha256'] == 'd9cbb4397afc231cf8250c371e25a36412abc3570e8cd3a4103a310aa0c3e67d'
    config = load(SESSION/'runtime-configuration.json')
    assert (config['status'],config['model'],config['reasoning']) == ('confirmed','gpt-6.1-sol','high')
    assert not (ROOT/'delivery.json').exists()
    selected = next(t for t in load('docs/work/queue.json')['tasks'] if t['id']=='IG-2B08')
    assert selected['status']=='in_progress'
    for k,v in TASK.items():
        if k!='status': assert selected[k]==v,k
    for c in load(SESSION/'packet.json')['control_files']:
        assert pin(c['path'])['sha256']==c['sha256']
    scope = load(TASK['repair_authorization']['scope']['path'])
    assert pin(scope['preserve_manifest']['path'])==scope['preserve_manifest']
    assert old_preservation()==19579
    old = scope['immutable_delivery']
    assert pin(old['path'])['sha256']==old['sha256']
    old_rows = load(old['path'])['artifacts']
    for p in old_rows: assert pin(p['path'])['sha256']==p['sha256']
    source = load(ROOT/'source-suite-execution.json')
    full = load(ROOT/'full-check-execution.json')
    cli = load(ROOT/'source-cli-validation.json')
    diff = load(ROOT/'diff-check-execution.json')
    qa = load(ROOT/'visual-qa.json')
    assert source['attempts'][-1]['exit_code']==full['attempts'][-1]['exit_code']==diff['exit_code']==0
    assert all(c['exit_code']==0 for c in cli['checks']) and len(cli['checks'])==3
    assert qa['all_sheets_inspected'] and qa['all_boundary_overlays_inspected'] and qa['exact_page33_context_inspected']
    assert load(ROOT/'batch-verification.json')['exit_code']==0
    assert load(ROOT/'arrow-completeness-report.json')['old_crop_rejected']
    assert load(ROOT/'F02-completeness-report.json')['old_crop_rejected']
    components = load(ROOT/'F03-F04-completeness-report.json')
    assert components['exit_code']==0
    assert all(c['old_crop_rejected'] and len(c['runs'])==3 for c in components['findings'].values())
    delta = load(ROOT/'repair-delta.json')
    assert delta['exit_code']==0 and delta['changed_region_count']==2
    generation = load(ROOT/'generation-execution.json')
    assert all(c['exit_code']==0 for c in generation['checks'])
    checks = [*generation['checks'],
        {'command':source['command'],'exit_code':0,'evidence':pin(ROOT/'source-suite-execution.json')},
        *cli['checks'],
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/probe_geometry.py','exit_code':0,'evidence':pin(ROOT/'geometric-content-probe.json')},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/check_arrow_completeness.py','exit_code':0,'evidence':pin(ROOT/'arrow-completeness-report.json')},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/check_hit_completeness.py','exit_code':0,'evidence':pin(ROOT/'F02-completeness-report.json')},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/check_component_completeness.py','exit_code':0,'evidence':pin(ROOT/'F03-F04-completeness-report.json')},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/verify_batch.py','exit_code':0,'evidence':pin(ROOT/'batch-verification.json')},
        {'command':full['command'],'exit_code':0,'evidence':pin(ROOT/'full-check-execution.json')},
        {'command':'git diff --check','exit_code':0,'evidence':pin(ROOT/'diff-check-execution.json')},
        {'command':'Fresh original pages, all authored boundaries/components and exact page-33 visual inspection','exit_code':0,'evidence':pin(ROOT/'visual-qa.json')},
        {'command':'Verify all current preservation manifest and frozen input delivery bytes before writes and at delivery','exit_code':0,'counts':{'preservation':19579,'old_delivery':len(old_rows)}}]
    started = load(ROOT/'checkpoint.json')['started_utc']
    ended = datetime.now(timezone.utc)
    measurement = {'started_utc':started,'ended_utc':ended.isoformat(),
        'elapsed_wall_seconds':(ended-datetime.fromisoformat(started)).total_seconds(),
        'input_tokens':None,'output_tokens':None,'operator_seconds':None,
        'unknown_reason':'Token counts and operator time were not exposed.',
        'observed_model':config['model'],'observed_reasoning':config['reasoning']}
    validation = {**meta,'summary':'F03/F04 complete intended components verified; F01/F02 regressions, complete independent serial replays, preservation, indexes and unchanged required suites passed.',
        'checks':checks,'measurement':measurement,'repair_findings':['F03','F04'],
        'repair_cycles':{'F03':1,'F04':1},'development_observations':pin(ROOT/'development-observations.json'),
        'source_suite':pin(ROOT/'source-suite-execution.json'),'repository_check':pin(ROOT/'full-check-execution.json'),
        'preserved_input_artifacts':19579,'prior_delivery_artifacts':len(old_rows),
        'defects_addressed':{'medium':1,'low':1},'independent_review':'Pending fresh supervisor-launched reviewer.',
        'semantic_acceptance_granted':False,'executable_readiness':False}
    write(ROOT/'validation-report.json',validation)
    handoff = '''# IG-2B08 F03/F04 repair delivery

The intended page-29 Tribune/V-counter detail uses [173,332,215,370] PDF points,
retaining the complete label, artwork, 0 field and marker frame. The later C
3-marker uses [455,390,490,426], retaining the digit and every exposed frame edge.
Full original-component pixel regressions reject both old clips and independent
edge truncations in final and both complete replays. Resolved F01 arrow and F02
4-marker regressions remain unchanged and pass.

Only those two zero-denominator authored selections and their dependent evidence
changed. All other selections, primary tiles, stable identities, registry history,
reading order, links and normalized non-target evidence are preserved. Every set
regenerated all 269 regions serially from the accepted baseline and persisted
registry. The accepted 44-page source set and nonassigned objects remain intact;
only the four authorized active placeholders are retired.

Fresh original pages 29-32, all boundaries/components and the exact page-33
[45,50,306,80] continuation crop were inspected. Page 28 was reference-only via
the authorized dependency projection. Context contributes zero denominator.
The full, assigned, inherited and context counts are separate in coverage-report.

The unchanged source suite, three task-bound source CLI validators, complete batch
and negative-case verifier, required repository check and git diff --check passed.
Actual commands, exits, private log pins and any approved execution are frozen.
All 19,579 preservation entries and the 10,255 prior delivery entries were verified
before writes and at freeze. All earlier attempts and deliveries remain immutable.

The initial Tribune preflight rejected five top-boundary reference pixels after
normalization; only its top margin was expanded by one point. Failure evidence is
retained. Tests, assertions, source scope, ACLs and global configuration are unchanged.
Machine transcription/descriptive gaps remain; formal semantics are unprocessed.
No semantic acceptance or gameplay readiness is granted. A fresh independent
reviewer must assess every original/appended criterion and frozen artifact hash.
Only the supervisor launches the next role.
'''
    (ROOT/'delivery-handoff.md').write_text(handoff,encoding='utf-8',newline='\n')
    pending = [c for c in TASK['acceptance'] if c.startswith('A fresh independent reviewer') or c.startswith('Independent review compares')]
    write(ROOT/'checkpoint-delivery.json',{**meta,'task':'IG-2B08','summary':'F03/F04 executor repair frozen for independent review.',
        'input_packet':pin(SESSION/'packet.json'),'repair_scope':TASK['repair_authorization']['scope'],
        'completed_criteria':[c for c in TASK['acceptance'] if c not in pending],
        'pending_criteria':pending,'checks':checks,'measurement':measurement,'blocker':None,
        'next_operation':'Transition the frozen delivery to review and stop this executor role.'})
    index = load(ROOT/'source-pins.json')
    current = {p['path']:p for p in index['current_reports']}
    for name in ('validation-report.json','delivery-handoff.md','checkpoint-delivery.json','visual-qa.json',
                 'F03-F04-completeness-report.json','source-cli-validation.json','source-suite-execution.json',
                 'full-check-execution.json','diff-check-execution.json','generation-execution.json',
                 'development-observations.json','original-access.json'):
        p=pin(ROOT/name);current[p['path']]=p
    index['current_reports']=list(current.values())
    artifacts={p['path']:p for p in index['artifacts']}
    # Explicit retained failed-proposal paths; no private tree traversal.
    for name in ('crop.pdf','image.png','text.txt'):
        p=pin(ROOT/'proposal-evidence/F03'/name);artifacts[p['path']]=p
    for p in qa['artifacts']:artifacts[p['path']]=p
    index['artifacts']=list(artifacts.values())
    write(ROOT/'source-pins.json',index)
    artifacts={}
    def collect(o):
        if isinstance(o,dict):
            if 'path' in o and 'sha256' in o:
                p=pin(o['path']);assert p['sha256']==o['sha256'],o['path']
                if 'bytes' in o:assert p['bytes']==o['bytes']
                artifacts[p['path']]=p
            for v in o.values():collect(v)
        elif isinstance(o,list):
            for v in o:collect(v)
    for o in (index,validation,qa,source,full,delta,components,
              load(ROOT/'preservation-report.json'),load(ROOT/'arrow-completeness-report.json'),
              load(ROOT/'F02-completeness-report.json'),load(ROOT/'proposal-preflight.json')):
        collect(o)
    collect(TASK['repair_authorization']);collect(scope['preserve_manifest']);collect(old)
    for name in ('runtime-configuration.json','task.json','packet.json','references.json',
                 'access-manifest.json','dependency-view.json','search-manifest.json'):
        p=pin(SESSION/name);artifacts[p['path']]=p
    for n in ('final-verified','replay-1','replay-2'):
        for name in ('inventory.json','identity-registry.json'):
            p=pin(ROOT/n/name);artifacts[p['path']]=p
    for f in ROOT.iterdir():
        if f.is_file() and f.name not in ('delivery.json','freeze-execution.log'):
            p=pin(f);artifacts[p['path']]=p
    for path in TASK['outputs']:assert path in artifacts,path
    ordered=[artifacts[p] for p in sorted(artifacts)]
    for p in ordered:assert pin(p['path'])==p
    coverage=load(ROOT/'coverage-report.json')
    envelope={**meta,'task':'IG-2B08','summary':'F03 Tribune and F04 3-marker intended evidence repaired; complete final and two serial replays, immutable baseline preservation, exhaustive evidence indexes and unchanged required checks passed. Independent review requested.',
        'criteria':TASK['acceptance'],'criteria_assessment':{'executor_deliverables':'Submitted for independent review.',
            'independent_review':'Pending.','human_semantic_acceptance':'Not granted; physical inventory only.',
            'executable_readiness':'Unverified.'},'artifacts':ordered,'checks':checks,
        'input_packet':pin(SESSION/'packet.json'),'repair_scope':TASK['repair_authorization']['scope'],
        'measurement':measurement,'preservation_manifest':scope['preserve_manifest'],
        'denominators':{'full_source':coverage['denominator_regions'],
            'assigned_four_pages':coverage['assigned_four_page']['denominator_regions'],
            'inherited_nonassigned':coverage['inherited_nonassigned']['denominator_regions'],
            'new_context_regions':coverage['context_only']['new_regions'],'context_contribution':0},
        'semantic_acceptance_granted':False,'executable_readiness':False,'preserved_input_artifact_count':19579,
        'excluded_scratch':['source-pytest/','__pycache__/','freeze-execution.log'],
        'next_operation':'Fresh independent review of all original/appended criteria and the exhaustive frozen artifact set.'}
    write(ROOT/'delivery.json',envelope)
    for p in ordered:assert pin(p['path'])==p
    assert old_preservation()==19579
    print(__import__('json').dumps({'delivery':pin(ROOT/'delivery.json'),'artifact_count':len(ordered),'preserved_input_artifacts':19579}))


if __name__=='__main__':
    main()
