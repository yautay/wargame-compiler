"""Freeze current executor delivery; never grant acceptance or edit prior runs."""
import importlib.metadata
import importlib.util
import json
import os
import sys
from datetime import datetime, timezone
from pathlib import Path
from prepare import ROOT, RUN, OLD, REVIEW, sha, write, pin, command

def freeze():
    config=json.loads((RUN/'configuration.json').read_text())
    q=json.loads((ROOT/'docs/work/queue.json').read_text()); before=json.loads((RUN/'queue-before.json').read_text())
    task=next(t for t in q['tasks'] if t['id']=='IG-2A'); assert task['status']=='in_progress'
    assert [t for t in q['tasks'] if t['id']!='IG-2A']==[t for t in before['tasks'] if t['id']!='IG-2A']
    checks=[]
    for name in ['sources-tests-03','verify-repair-01','inventory-one','inventory-two','real-evidence','source-and-pixel-oracle','project-check']:
        check=json.loads((RUN/(name+'.json')).read_text()); assert check['exit_code']==0; checks.append(check)
    checks.append(command('final-workflow-02',[sys.executable,'scripts/workflow.py','validate']))
    checks.append(command('final-diff-02',['git','diff','--check']))
    assert all(c['exit_code']==0 for c in checks)
    review=json.loads((REVIEW/'review-manifest.json').read_text())['artifacts']
    for e in review: assert sha(ROOT/e['path'])==e['sha256']
    old=json.loads((OLD/'delivery.json').read_text())['artifacts']
    intentional={'docs/work/context-policy.json','contracts/ig/regions.schema.json','src/wgc/sources/inventory.py',
                 'src/wgc/sources/pdf.py','src/wgc/sources/geometry.py','src/wgc/sources/README.md'}
    for e in old:
        assert sha(RUN/'original-delivery'/e['path'])==e['sha256']
        if e['path'] not in intentional: assert sha(ROOT/e['path'])==e['sha256']
    for e in json.loads((RUN/'frozen-tools.json').read_text()): assert sha(ROOT/e['path'])==e['sha256']
    write('preservation-final.json',{'original_delivery_snapshots_verified':len(old),'unchanged_live_old_delivery_artifacts':len(old)-len(intentional),
          'intentional_superseded_live_paths':sorted(intentional),'independent_review_artifacts_unchanged':len(review),
          'workflow_and_ig1a_contract_unchanged':True,'other_38_task_records_unchanged':True,
          'source_pdf_unchanged':True,'old_runs_and_inventory_unchanged':True,
          'original_delivery_json_copy':pin(RUN/'original-delivery'/((OLD/'delivery.json').relative_to(ROOT))),
          'source_pdf':pin(ROOT/'private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf')})
    tc=json.loads((OLD/'toolchain.json').read_text()); libs={n:importlib.metadata.version(n) for n in tc['libraries']}
    assert libs==tc['libraries']
    exes={k:pin(Path(v['path'])) if Path(v['path']).is_relative_to(ROOT) else {'path':v['path'],'sha256':sha(Path(v['path']))} for k,v in tc['executables'].items()}
    differences=[{'name':k,'expected_previous_sha256':tc['executables'][k]['sha256'],
                  'observed_current_sha256':exes[k]['sha256']} for k in exes
                 if exes[k]['sha256']!=tc['executables'][k]['sha256']]
    runtime_path=Path('C:/Users/yauta/.cache/codex-runtimes/codex-primary-runtime/runtime.json')
    runtime=json.loads(runtime_path.read_text())
    write('toolchain.json',{'python_executable':sys.executable,'python_version':sys.version,'libraries':libs,'executables':exes,
          'process_pythonpath':os.environ.get('PYTHONPATH'),'process_path_poppler':str(Path(tc['executables']['pdfinfo']['path']).parent),
          'installs':0,'global_config_changes':0,'prior_toolchain':pin(OLD/'toolchain.json'),
          'previous_bundle_version':tc['bundle_version'],'current_runtime_metadata':runtime,
          'binary_differences':differences,'starting_executable_hashes':None,
          'observation_limit':'Executable hashes captured during freeze, not before execution. Current file timestamps precede run start; runtime manifest indicates a newer bundle. This supports a pre-session replacement inference, not authenticated update provenance.',
          'validation_basis':'Current bundle permitted by operator; current tests, count, canonical replay and independent pixel oracles passed. Prior expected executable hashes are preserved, not overwritten.'})
    image_records=[]
    for number in range(1,5):
        image_records.append({'physical_page':number,'image':pin(RUN/f'd/page-{number:02d}.png'),
                             'observed_printed_label':None if number==1 else str(number),
                             'label_location':None if number==1 else ('top-right' if number==3 else 'top-left'),
                             'visible_clipping':False})
    write('visual-inspection.json',{'actor':config['actor'],'method':'Current executor viewed all four fresh original-source PNGs with view_image',
          'pages':image_records,'edition_observation':'5th Edition visible on physical page 1','cover_label_status':'unknown',
          'pages_5_44_content_access':False,'source_meaning_review':False,'semantic_acceptance_granted':False})
    dispositions=json.loads((RUN/'dispositions-before.json').read_text())
    for f in dispositions:
        f.update(disposition='repair_implemented_pending_independent_review',repair_cycles=1,
                 closure_evidence=[pin(RUN/'repair-probes.json'),pin(RUN/'sources-tests-03.json'),pin(RUN/'geometry-oracle.json')],
                 independent_closure='Not granted by this executor; new independent review must assess these exact bytes.')
    write('dispositions.json',dispositions)
    criteria=[{'criterion':c,'status':'met_for_tooling_scope_pending_independent_review',
               'evidence':[pin(RUN/n) for n in ['repair-probes.json','sources-tests-03.json','repeatability.json','source-audit.json','geometry-oracle.json','verified-coverage.json']],
               'limitations':'Structural validity and source associations only; no substantive IG-2B inventory, human authentication, semantic acceptance or executable readiness.'} for c in task['acceptance']]
    write('criteria.json',criteria)
    write('checks.json',checks)
    write('development-failures.json',{'retained_failed_commands':[pin(RUN/n) for n in ['sources-tests-01.json','sources-tests-02.json']],
          'failures':[{'kind':'Test collection import','resolution':'Use pytest importlib package name tests.sources.test_inventory','resolved':True},
                      {'kind':'New positive label test retained reference to old page after reseal','resolution':'Update current document page, preserving the assertion','resolved':True}],
          'product_regressions_detected_after_repair':0,'assertions_weakened':False,
          'preliminary_shell_errors':['Attempted explicit read of nonexistent src/wgc/sources/identity.py; actual inventory.py owns registry',
                                      'Attempted read of project-check.stdout before subprocess completion; subsequently captured completed output'],
          'measurement_note':'Preliminary direct reads did not have retained per-command clock records; not reported as passing checks.'})
    products=[ROOT/e['path'] for e in json.loads((RUN/'base-products.json').read_text())]
    products += [ROOT/'tests/sources/test_review_repairs.py']
    changed=[]
    base={e['path']:e['sha256'] for e in json.loads((RUN/'base-products.json').read_text())}
    for p in products:
        record=pin(p)
        if record['path'] not in base or record['sha256']!=base[record['path']]: changed.append(record)
    write('changed-products.json',changed)
    end=datetime.now(timezone.utc); start=datetime.fromisoformat(config['started_utc'])
    measurement={'started_utc':start.isoformat(),'ended_utc':end.isoformat(),'wall_seconds':(end-start).total_seconds(),
                 'input_tokens':None,'output_tokens':None,'cost':None,'operator_seconds':None,
                 'unknown_reason':'Task token/cost counters and operator time unavailable; preliminary reads before captured start are unmeasured.',
                 'actual_model':config['model'],'actual_reasoning':config['reasoning'],'actor':config['actor']}
    write('measurement.json',measurement)
    write('checkpoint.json',{'task':'IG-2A','actor':config['actor'],'configuration':pin(RUN/'configuration.json'),
          'input_packet':pin(RUN/'packet-manifest.json'),'base_products':json.loads((RUN/'base-products.json').read_text()),
          'changed_products':changed,'criteria':criteria,'checks':checks,'blocker':None,
          'next_operation':'Freeze delivery; transition in_progress to review; separate independent review of new hashes.'})
    report=f'''# IG-2A bounded repair delivery

Outcome: repair implemented; independent review pending. Executor {config['actor']}, current-session GPT-6.1 Sol / high confirmed directly by the operator. No acceptance/done or semantic acceptance.

All five findings were independently reproduced before changes (10 invalid cases accepted, two valid baselines accepted). Coordinator dispositions and review-to-changes_requested evidence are preserved. All 87 old delivery artifacts were verified and copied byte-for-byte before product edits. The sealed review's 159 artifacts, frozen workflow tools and IG-1A schema/validator/README remain unchanged. Only IG-2A queue scope/context and necessary allowlist/generated views were coordinated.

R01 binds every evidence derivation to page identity, physical address, source revision, boxes, effective crop, rotation and UserUnit, independent of labels. Root validation verifies actual byte-pinned PDF count and geometry. R02 checks DPI/physical crop/rotation against Poppler ceiling pixel dimensions and the PNG header. R03 requires verified label evidence on the same current physical page. R04 pins full author/registry/page/partition scope outside coverage hashing; source-IG review freshness remains unknown and human authority unverified. R05 checks real pypdf/Poppler count and binds physical-page keys to their physical addresses. Registry replay retains UUIDs; changed-PDF registry reuse remains refused.

Validation: 71 sources tests, 102 project tests, 17 migrated/own probes all passed. Two fresh 44-page structural inventories using the persisted registry have identical canonical bytes/identities, also identical to the prior seed. Four fresh page PNGs match independent original-PDF renders pixel-for-pixel. Four asymmetric crop/rotation/UserUnit pixel oracles pass; eight additional fractional-unit/origin/DPI/rotation tests pass. Exact commands, exits, errors and subprocess times are retained in checks.json and named logs. The two failed test-development attempts are retained with their fixes; expectations were not weakened. check.ps1 ran unchanged with an output-only adapter that keeps operational logs/scratch in this repair run. Schema JSON keeps its original CRLF byte style; parsed content was unchanged by that final format restoration.

Every acceptance criterion is assessed in criteria.json as met for the tooling scope pending independent review. All 44 placeholders remain unprocessed; none count as represented. Content extraction/inspection was limited to physical pages 1-4. Cover label and labels 5-44 remain unknown. No substantive IG-2B inventory was executed. Exact source-IG whole-record exclusion review and human decision authentication remain separate future obligations; sidecar scope validation grants neither.

Residual limits: pypdf's pre-existing non-zero-indexed Xref warning remains logged; original source bytes are unchanged. Validation without root checks internal consistency and explicitly leaves source structure unverified. Old evidence missing the new required page basis must be freshly derived, not resealed to invent freshness. This attempt regenerates evidence instead of modifying frozen old inventories. Registry provenance and human claims are not authenticated by a self-consistent document. Current runtime bundle {runtime['bundleVersion']} differs from prior bundle {tc['bundle_version']}: both Poppler EXE hashes differ while version strings and library versions match. Exact previous/current hashes are retained in toolchain.json and toolchain-change-observations.json; no old expectation was changed. Current native executable timestamps precede the run, supporting a pre-session replacement inference. Starting executable hashes were not captured. All current count/replay/render/oracle checks passed using the permitted existing local bundle. The first freeze failed on this difference and is recorded separately.

UTC start {measurement['started_utc']}; freeze {measurement['ended_utc']}; elapsed {measurement['wall_seconds']:.3f} seconds. Preliminary reads before the captured start are unmeasured. Tokens, cost and operator time are null.

Next action: operator supplies this new frozen delivery/manifest/handoff to a separate independent reviewer. Review exact new hashes and all five closure conditions; do not accept/done from this executor session or execute IG-2B.
'''
    (RUN/'delivery-handoff.md').write_text(report,encoding='utf-8',newline='\n')
    scratch={'t1','t2','t3'}
    artifacts=[]
    for p in sorted(RUN.rglob('*')):
        if not p.is_file(): continue
        rel=p.relative_to(RUN)
        if rel.parts[0] in scratch or rel.parts[:2] in [('c','pytest'),('c','temp')]: continue
        if p.name in {'delivery.json','delivery-manifest.json','final-seal.json'}: continue
        artifacts.append(pin(p))
    artifacts += [pin(p) for p in products] + [pin(ROOT/'docs/work/context-policy.json')]
    write('delivery-manifest.json',{'format':'wgc-delivery-manifest-1','task':'IG-2A','actor':config['actor'],
          'artifacts':artifacts,'criteria':criteria,'checks':checks,'measurement':measurement,
          'excluded_operational_scratch':['t1/','t2/','t3/','c/pytest/','c/temp/'],
          'changed_products':changed,'independent_review':'pending','semantic_acceptance_granted':False})
    delivery={'role':'executor','actor':config['actor'],'summary':'Frozen repair of confirmed IG2A-R01 through R05; separate independent technical review required.',
              'criteria':task['acceptance'],'artifacts':artifacts+[pin(RUN/'delivery-manifest.json')],
              'model':config['model'],'reasoning':config['reasoning'],'configuration_evidence':(RUN/'configuration.json').relative_to(ROOT).as_posix(),
              'checks':checks,'measurement':measurement,'independent_review':'pending','semantic_acceptance_granted':False}
    write('delivery.json',delivery)
    for e in delivery['artifacts']: assert sha(ROOT/e['path'])==e['sha256']
    print('Frozen delivery:',len(delivery['artifacts']),'artifacts;',len(changed),'changed product files.')

if __name__=='__main__': freeze()
