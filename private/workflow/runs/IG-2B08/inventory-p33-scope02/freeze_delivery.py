"""Freeze this owned attempt only after all required validations and visual QA."""
from datetime import datetime, timezone
from pathlib import Path
import json
from build_inventory import ROOT, SESSION, TASK, SPECS, load, write, pin, metadata, old_preservation


def main():
    meta=metadata()
    config=load(SESSION/'runtime-configuration.json')
    assert (config['status'],config['model'],config['reasoning'])==('confirmed','gpt-6.1-sol','high')
    assert meta['configuration_sha256']=='91c91c99f5e1dcfbbe51c3fb6c5f7f8550d273ad07df5dc2e4d15608f0c2aa21'
    assert not (ROOT/'delivery.json').exists()
    # Queue access is internal to this final check, with no event/dependency dump.
    selected=next(t for t in load('docs/work/queue.json')['tasks'] if t['id']=='IG-2B08')
    assert selected['status']=='in_progress'
    for field,value in TASK.items():
        if field!='status':assert selected[field]==value,field
    for control in load(SESSION/'packet.json')['control_files']:
        assert pin(control['path'])['sha256']==control['sha256'],control['path']
    source=load(ROOT/'source-suite-execution.json');full=load(ROOT/'full-check-execution.json')
    assert source['approved_attempt']['exit_code']==0 and full['attempts'][-1]['exit_code']==0
    cli=load(ROOT/'source-cli-validation.json');assert all(x['exit_code']==0 for x in cli['checks'])
    batch=load(ROOT/'batch-verification.json');assert batch['exit_code']==0
    qa=load(ROOT/'visual-qa.json');assert qa['all_sheets_inspected'] and qa['exact_page33_context_inspected']
    assert old_preservation()==25
    preservation=load(ROOT/'preservation-report.json');coverage=load(ROOT/'coverage-report.json')
    names=('final-verified','replay-1','replay-2')
    checks=[
        {'command':'Local exact packet/control/input/runtime hash verification; 25 preserved old-attempt artifact pins; absent-owned-directory verification','exit_code':0},
        {'command':'Final selected queue contract/status ownership check and packet control-file/runtime hash revalidation','exit_code':0},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/inspect_originals.py','exit_code':0},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/author_specs.py','exit_code':0},
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/build_inventory.py prepare','exit_code':0},
        *[{'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/build_inventory.py {name}','exit_code':0} for name in names],
        {'command':source['command'],'exit_code':0,'execution':'Approved exact unchanged command after documented Windows restricted-token temp access denial.','evidence':pin(ROOT/'source-suite-execution.json')},
        *cli['checks'],
        {'command':f'.venv/Scripts/python.exe {ROOT.as_posix()}/verify_batch.py','exit_code':0,'evidence':pin(ROOT/'batch-verification.json')},
        {'command':'pwsh -NoProfile -File scripts/check.ps1 -Task IG-2B08','exit_code':0,'execution':'Approved exact unchanged command; 288 tests passed.','evidence':pin(ROOT/'full-check-execution.json')},
        {'command':'git diff --check','exit_code':0,'evidence':pin(ROOT/'diff-check-execution.json')},
        {'command':'Fresh visual review of every assigned original, proposed boundary overlay, component sheet and exact page-33 crop','exit_code':0,'evidence':pin(ROOT/'visual-qa.json')},
    ]
    started=load(ROOT/'checkpoint.json')['started_utc'];ended=datetime.now(timezone.utc)
    measurement={'started_utc':started,'ended_utc':ended.isoformat(),'elapsed_wall_seconds':(ended-datetime.fromisoformat(started)).total_seconds(),
        'operator_seconds':None,'input_tokens':None,'output_tokens':None,'unknown_reason':'Token and operator-time measurements were not exposed.',
        'executor':meta['actor'],'reviewer':None,'requested_model':'gpt-6.1-sol','requested_reasoning':'high','observed_model':config['model'],'observed_reasoning':config['reasoning']}
    validation={**meta,'summary':'All required unchanged suites and three source CLI validations passed; serial evidence, complete replays, preservation and index checks passed.',
        'checks':checks,'restricted_token_failures':[{'command':source['command'],'exit_code':1,'resolution':'Approved unchanged exact command passed; no ACL/library/test changes.'},
            {'command':full['attempts'][0]['command'],'exit_code':1,'resolution':'Approved unchanged exact command passed; no assertion or guard changes.'}],
        'derivation_failure':pin(ROOT/'derivation-repair-01.json'),'verifier_failure':pin(ROOT/'verifier-repair-01.json'),'component_correction':pin(ROOT/'component-correction-01.json'),'metadata_decode_failure':pin(ROOT/'metadata-decode-repair-01.json'),'old_attempt_pins_verified':25,'retries':{'source_suite':1,'full_check':1,'owned_path_helper':1,'verifier_missing_import':1,'detail_crop_correction':1,'metadata_decode':1},
        'defects':{'owned_helper_errors_fixed':3,'visual_detail_crop_corrected':1,'unresolved_model_review_findings':0,'independent_review_pending':True},
        'measurement':measurement,'human_semantic_acceptance_granted':False,'gameplay_readiness':'unverified'}
    write(ROOT/'validation-report.json',validation)
    handoff=f'''# IG-2B08 delivery for independent review

Fresh source inventory of physical pages 29-32, preserving the full accepted
44-page baseline. Exactly four active placeholders were retired; all 937 retained
region objects, 925 existing evidence objects, 229 links, registry bindings and
retained reading-order subsequence were preserved. Old blocked attempt: all 25
artifact pins verified again; no drafts, old inspections or tests inherited.

The fresh set contains 183 disjoint primary inventory regions, 85 overlapping
assigned-page visual detail regions with zero denominator, and one exact page-33
boundary region with zero denominator. All 269 regions have fresh crop PDF, PNG,
clipped original-page text and exact locator metadata. Both independent replays
regenerated all 269 regions serially from the accepted baseline and persisted
author registry. IDs, author fields, registry, order, links and normalized artifact
bytes/locators match; actual inventory hashes remain path-dependent.

All required checks passed: 71 source tests, 288 full-suite tests, three source-backed
CLI validations, owned complete verifier and git diff --check. Approved execution
resolved the two restricted-token temporary-directory failures without changing
tests, guards, assertions, libraries or ACLs. The helper path failure and its three
partial files are preserved. A report-assembly missing import was corrected and the
complete verifier rerun. See validation-report.json for commands/exits.
Visual QA also corrected one D-locator detail crop. All 2,427 superseded derivative
files were retained and all three complete sets regenerated with the corrected
author selection before the final verification and freeze.
The final ownership check also caught locale-dependent decoding of the task title
in the owned helper. Explicit UTF-8 decoding resolved it; direct UTF-8 comparison
confirmed every selected non-status contract field already matched the queue.

Coverage remains explicit: machine punctuation and counter glyphs are unverified,
descriptive semantics are partial, formal semantics are unprocessed, geometric
spacing/margins and 29 overhang pixels remain recorded gaps. Context contributes
zero denominator. No human semantic acceptance or executable readiness is granted.
Page 28 was reference-only through the prepared accepted boundary projection;
page 33 was inspected solely within the exact [45,50,306,80] point rectangle.

Next action: a fresh independent reviewer must inspect every assigned original,
proposed boundary/component, exact context boundary and complete ledger against
delivery.json; recheck preservation, exhaustive indexes and both complete replays.
This executor has not performed that independent review and starts no next task.
'''
    (ROOT/'delivery-handoff.md').write_text(handoff,encoding='utf-8',newline='\n')
    write(ROOT/'checkpoint-delivery.json',{**meta,'task':'IG-2B08','attempt':ROOT.name,
        'summary':'Complete bounded source inventory and validation ready to freeze for fresh independent review.',
        'input_packet':pin(SESSION/'packet.json'),'source_revisions':[load(ROOT/'author-inventory.json')['source']['sha256']],
        'changed_file_hashes':[pin(ROOT/n/'inventory.json') for n in names],
        'completed_criteria':[c for c in TASK['acceptance'] if not c.startswith('A fresh independent reviewer') and not c.startswith('Independent review compares')],
        'pending_criteria':[c for c in TASK['acceptance'] if c.startswith('A fresh independent reviewer') or c.startswith('Independent review compares')],
        'commands':checks,'blocker':None,'next_operation':'Transition frozen delivery to review; supervisor launches the independent reviewer.','measurement':measurement})
    index=load(ROOT/'source-pins.json')
    current={p['path']:p for p in index['current_reports']}
    for name in ('validation-report.json','delivery-handoff.md','checkpoint-delivery.json','visual-qa.json','source-cli-validation.json','source-suite-execution.json','full-check-execution.json','diff-check-execution.json'):
        p=pin(ROOT/name);current[p['path']]=p
    index['current_reports']=list(current.values())
    indexed={p['path'] for p in index['artifacts']}
    for p in qa['artifacts']:
        if p['path'] not in indexed:index['artifacts'].append(p);indexed.add(p['path'])
    write(ROOT/'source-pins.json',index)
    # No tree search: gather declared pins plus exact owned root files and the
    # preserved partial derivative. Pytest scratch and bytecode are not deliverables.
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
    collect(index);collect(validation);collect(preservation);collect(qa)
    collect(load(ROOT/'component-correction-01.json'))
    for name in ('runtime-configuration.json','task.json','packet.json','references.json','access-manifest.json','dependency-view.json','search-manifest.json'):
        p=pin(SESSION/name);artifacts[p['path']]=p
    for n in names:
        for file in ('inventory.json','identity-registry.json'):
            p=pin(ROOT/n/file);artifacts[p['path']]=p
    partial=ROOT/'failed-path-pin-01/evidence/ig2b08-p29-running-header'
    for file in ('crop.pdf','image.png','text.txt'):
        p=pin(partial/file);artifacts[p['path']]=p
    for file in ROOT.iterdir():
        if file.is_file() and file.name!='delivery.json':
            p=pin(file);artifacts[p['path']]=p
    for path in TASK['outputs']:assert path in artifacts,path
    ordered=[artifacts[path] for path in sorted(artifacts)]
    for p in ordered:assert pin(p['path'])==p
    envelope={**meta,'task':'IG-2B08','summary':'Fresh IG-2B08 four-page inventory delivered with complete evidence, two full independent replays, exact 44-page preservation and passing unchanged checks; independent review requested.',
        'criteria':TASK['acceptance'],'criteria_assessment':{'executor_deliverables':'Complete and submitted for independent review.','independent_review':'Pending in fresh supervisor-launched reviewer role.','human_semantic_acceptance':'Not granted or required for this physical inventory task.','source_meaning':'Unaccepted; transcription/descriptive gaps remain.','executable_readiness':'Unverified.'},
        'artifacts':ordered,'checks':checks,'input_packet':pin(SESSION/'packet.json'),'measurement':measurement,
        'denominators':{'full_source':coverage['denominator_regions'],'assigned_four_pages':183,'inherited_nonassigned':coverage['inherited_nonassigned']['denominator_regions'],'new_context_regions':86,'context_contribution':0},
        'semantic_acceptance_granted':False,'next_operation':'Fresh independent reviewer checks all original/appended criteria against this exact exhaustive frozen artifact set.',
        'excluded_scratch':['source-pytest/','__pycache__/'],'preserved_old_attempt_artifact_count':25}
    write(ROOT/'delivery.json',envelope)
    for p in envelope['artifacts']:assert pin(p['path'])==p
    print(json.dumps({'delivery':pin(ROOT/'delivery.json'),'artifact_count':len(ordered),'old_attempt_preserved':old_preservation()}))


if __name__=='__main__':main()
