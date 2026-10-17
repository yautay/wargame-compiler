"""Attempt-local freezing, path-policy preflight and post-review handoff/seal.

Status transitions and packet creation remain explicit calls to unchanged workflow.py.
No command in this module changes the real queue, source, contracts or prior attempts.
"""
import argparse
import copy
from datetime import datetime
from importlib.machinery import SourceFileLoader
import json
import os
from pathlib import Path
import re
import sys

u = SourceFileLoader('repair_common', str(Path(__file__).with_name('repair-common.py'))).load_module()
w = SourceFileLoader('workflow_controls', str(u.R/'scripts/workflow.py')).load_module()
POSTFREEZE_LABELS = ('freeze-delivery','delivery-envelope-preflight','review-transition',
                     'inspect-review-transition','review-packet','post-review-workflow-validate',
                     'post-review-diff-check','prepare-rereview')
CURRENT_NAMES = ['authored/inventory.json','authored/identity-registry.json','final-verified/inventory.json',
                 'final-verified/identity-registry.json','final-verified/coverage.json',
                 'author-specifications-final.json','component-observations.json','region-ledger-final.json',
                 'visual-inspection.json','source-observations.json','finding-dispositions.json','affected-component-audit.json',
                 'delta-audit.json','preservation-report.json','report-consistency-audit.json','replay-report.json',
                 'scope-report-final.json','context-authored-correspondence.json','continuations.json',
                 'uncertainty.json','gaps.json','geometric-gaps.json','locator-audit.json','coverage-report.json',
                 'criteria.json','configuration.json','toolchain.json','required-checks.json','repair-plan.json']

def queue():
    q=u.load(u.R/'docs/work/queue.json')
    return q,next(t for t in q['tasks'] if t['id']=='IG-2B02')

def preflight(artifacts):
    seen=set()
    for a in artifacts:
        p=w.safe_path(u.R,a['path'])
        assert not w.denied(a['path']), a['path']
        assert p.is_file() and w.digest(p)==a['sha256'] and p.stat().st_size==a['bytes'], a
        assert a['path'] not in seen, a['path']
        seen.add(a['path'])
    return len(seen)

def checkpoint_snapshot(name,stage,next_operation,exclude=()):
    cp=u.load(u.A/'checkpoint.json')
    cp.update(stage=stage,updated_utc=u.now(),blocker=None,next_operation=next_operation)
    cp['owned_current_hashes']=[u.pin(p) for p in sorted(u.A.rglob('*'))
                               if p.is_file() and p.name!='checkpoint.json' and p.name not in exclude]
    cp['current_status_observation']=queue()[1]['status']
    (u.A/'checkpoint.json').write_bytes(u.encoded(cp))
    with (u.A/name).open('xb') as f:f.write(u.encoded(cp))
    return u.pin(u.A/name)

def observe_config():
    cfg=u.CFG
    assert os.environ['CODEX_SESSION_ID']==cfg['session_id']
    records=[]
    for i,line in enumerate(Path(cfg['evidence_source']).open(encoding='utf-8'),1):
        d=json.loads(line)
        if d.get('type') not in ('session_meta','turn_context'):continue
        x=d['payload']
        keys=('id','timestamp','cwd','originator','cli_version','source','model_provider','model','effort','reasoning_effort')
        records.append(dict(line=i,record_type=d['type'],raw_record_sha256=u.hashlib.sha256(line.encode()).hexdigest(),
                            observed={k:x[k] for k in keys if k in x}))
    assert records[0]['observed']['id']==cfg['session_id']
    turns=[r for r in records if r['record_type']=='turn_context']
    assert turns and all(r['observed'].get('model')=='gpt-6.1-sol' and r['observed'].get('effort')=='high' for r in turns)
    u.write(u.A/'configuration-reobservation.json',dict(actor=cfg['actor'],session_id=cfg['session_id'],
            model='gpt-6.1-sol',reasoning='high',observed_utc=u.now(),configuration=u.pin(u.A/'configuration.json'),
            records=records,scope='Own configuration/identity records only.'))

def verify_prepared_pins():
    count=0
    for ln in (u.P/'repair-launch.txt').read_text(encoding='utf-8').splitlines():
        m=re.fullmatch(r'([^|]+) \| (\d+) \| ([a-f0-9]{64})',ln)
        if not m:continue
        path,n,d=m.groups();x=dict(path=path.strip(),bytes=int(n),sha256=d)
        if x['path']=='docs/work/queue.json':
            assert u.sha(u.C/'queue-before.json')==d and (u.C/'queue-before.json').stat().st_size==int(n)
        else:u.verify(x)
        count+=1
    assert count==69
    return count

def freeze():
    q,t=queue();assert t['status']=='in_progress' and q==u.load(u.A/'queue-in-progress.json')
    assert t['events'][-1]['sha256']==u.sha(u.A/'claim.json')
    assert u.load(u.A/'postrepair-frozen-bases.json')['frozen_unique_refs_verified']==4246
    assert u.load(u.A/'complete-metadata-audit.command.json')['exit_code']==0
    verify_prepared_pins();observe_config()
    checks=u.load(u.A/'required-checks.json')['checks']
    assert all(c['exit_code']==0 for c in checks)
    extra_labels=('complete-metadata-audit','postrepair-frozen-bases','repair-replay-one','repair-replay-two','observe-toolchain-v2')
    checks += [u.load(u.A/(s+'.command.json')) for s in extra_labels]
    assert all(c['exit_code']==0 for c in checks)
    check_stdout=(u.A/'repository-check.stdout').read_text(encoding='utf-8')
    check_root=Path(re.search(r'^LOG_ROOT=(.+)$',check_stdout,re.M).group(1).strip())
    assert check_root.resolve().is_relative_to((u.R/'private/workflow/checks').resolve())
    check_logs=[u.pin(check_root/n) for n in ('result.json','plan.log','dry-run.log','pytest.log','diff-check.log')]
    result=u.load(check_root/'result.json')
    assert all(result[k]==0 for k in ('plan_exit','dry_run_exit','tests_exit','diff_exit'))
    assert '102 passed' in check_stdout and '71 passed' in (u.A/'source-tests.stdout').read_text()
    u.write(u.A/'check-output-pins.json',dict(repository_check_root=check_root.relative_to(u.R).as_posix(),
            exact_log_files=check_logs,fixture_policy='Synthetic pytest temporary trees are not product artifacts; all result/root logs pinned.',
            source_tests=71,full_suite_tests=102))
    exclusion_names=[s+ext for s in POSTFREEZE_LABELS for ext in ('.command.json','.stdout','.stderr')]
    cp=checkpoint_snapshot('pre-delivery-checkpoint.json','delivery_prepared',
                           'Freeze envelope, policy-preflight every artifact, single review transition.',exclude=exclusion_names)
    current={n:u.pin(u.A/n) for n in CURRENT_NAMES}
    handoff='''# IG-2B02 bounded R01/R02 repair delivery

The new repair changes exactly three component arrays: Alae lower-left 6 to literal 5,
and a literal small white 1 after Thrace in each of the distinct light-infantry and
javelinists counter descriptions. All other descriptions/order and uncertain identifier
strings are retained. All 141 ledger entries are supplied; seven pre-existing overrides
are preserved. The single effective-components rule is recorded in repair-plan.json.

Five canonical snapshot files are byte-identical to the reviewed base. All source/region
IDs, revisions, boxes, labels, memberships, reading order, links, old context, accepted
pages 1-4, placeholders 9-44 and 423 primary raw files retain exact bytes/references.
Task counts 39/33/39/30 = 141, full 130+36+141 = 307; context denominator zero.
Transcription stays partial and descriptive/formal semantics unprocessed with gaps.

Only the three exact pinned counter PNGs and reviewer original-derived enlargements
were viewed in this session. Other original observations are explicitly attributed to
their immutable executor/reviewer inputs. No full or adjacent page content was viewed.
Source PDF access here was byte-hashing and unchanged 44-page structural validation.

Fresh checks: root validator, 71 source tests, scripts/check.ps1 (102 tests), workflow
validation, git diff --check, full metadata/preservation/consistency audit, two exact
replays and all 4246 frozen references before/after. Xref and Git warnings are retained.
One tool-banner comparison failed on CRLF versus original text-mode LF; that failure,
the original script and changed hypothesis are preserved, followed by a passing check.

Criterion 1: executor-repaired_pending_independent_review. Criterion 5: pending fresh
independent session. No acceptance, semantic approval, done or downstream work.
The operator separately authorizes a fresh independent reviewer of all original pages
5-8 and the complete new delivery. This actor does not create/message that reviewer.

Current repaired targets and reports (old corresponding metadata is historical only):
'''
    for name,p in current.items():handoff+=f"\n- {p['path']} | {p['bytes']} bytes | SHA256 {p['sha256']}"
    handoff+='\n\nActor: '+u.CFG['actor']+'; actual model gpt-6.1-sol, reasoning high, from own session metadata.\n'
    handoff+='Configuration proof: '+json.dumps(u.pin(u.A/'configuration-reobservation.json'))+'\n'
    handoff+='Immutable pre-delivery checkpoint: '+json.dumps(cp)+'\n'
    handoff+='\nTokens, monetary cost and operator time are unavailable (null), not estimated.\n'
    handoff+='\nCycle policy: manifest excludes itself/envelope/final seal, mutable checkpoint and post-freeze outputs; final seal pins the latter after real review event/packet. Sealed files are never rewritten.\n'
    with (u.A/'delivery-handoff.md').open('x',encoding='utf-8',newline='\n') as f:f.write(handoff)
    excluded={'checkpoint.json',*exclusion_names}
    new=[u.pin(p) for p in sorted(u.A.rglob('*')) if p.is_file() and p.name not in excluded]
    catalogue=u.load(u.P/'frozen-base-pins.json')['frozen_pins']
    immutable={};metadata_only=[]
    for x in catalogue:
        u.verify(x)
        try:
            p=w.safe_path(u.R,x['path'])
            assert not w.denied(x['path'])
        except (ValueError,AssertionError):
            metadata_only.append(x);continue
        immutable[x['path']]=x
    h=u.load(u.C/'coordinator-handoff.json')
    extra=[u.P/'preparation.json',u.P/'repair-scope.json',u.P/'repair-launch.txt',u.P/'frozen-base-pins.json',
           u.P/'verify-frozen-bases.py',u.P/'coordinator-queue-patch-v2.json',u.P/'independent-rereview-template.txt',
           u.C/'coordinator-handoff.json',u.C/'authorization.json',u.C/'coordinator-decision.json',
           u.C/'queue-before.json',u.C/'queue-scoped-review.json',u.C/'queue-changes-requested.json',
           u.R/h['packet']['manifest']['path'],u.R/h['packet']['context']['path']]
    for p in extra:immutable[u.pin(p)['path']]=u.pin(p)
    for x in check_logs:immutable[x['path']]=x
    inputs=[immutable[k] for k in sorted(immutable)]
    n=preflight(new+inputs)
    u.write(u.A/'delivery-preflight.json',dict(outcome='passed',workflow=u.pin(u.R/'scripts/workflow.py'),
            unchanged_rules=['safe_path','denied','is_file','digest','bytes'],preflight_artifact_count=n,
            native_or_denied_paths_kept_only_inside_toolchain_or_frozen_catalogue_metadata=len(metadata_only),
            live_queue_equals_immutable_in_progress_snapshot=True,original_pin_table_reverified=69,
            policy='This report excludes itself/manifest/envelope; freeze function policy-checks those final pins after writing, and a separate post-freeze envelope-preflight checks EVERY final artifact before transition.'))
    new.append(u.pin(u.A/'delivery-preflight.json'));preflight(new+inputs)
    manifest=dict(format='wgc-frozen-bounded-repair-delivery-1',task='IG-2B02',actor=u.CFG['actor'],created_utc=u.now(),
                  new_reviewed_artifacts=new,immutable_inputs_and_old_evidence=inputs,
                  metadata_only_native_observations=metadata_only,current_targets=current,
                  immutable_baseline_catalogue=u.pin(u.P/'frozen-base-pins.json'),
                  baseline_policy='Every original delivery/review/preparation artifact is immutable input or historical process evidence; old defective specifications/components/ledger/visual reports are never new current targets.',
                  current_report_policy='current_snapshot/current_component_authority select new attempt. baseline_payload/internal old paths are explicitly immutable original attribution.',
                  historical_process_evidence=['observe-toolchain-failed-v1.py','observe-toolchain.command.json','observe-toolchain.stdout','observe-toolchain.stderr','toolchain-comparison-hypothesis.json'],
                  self_exclusion_policy='Manifest excludes itself, delivery.json, final-seal.json and mutable checkpoint.json to avoid cycles. Envelope pins manifest plus full ordered lists. Immutable stage checkpoints are pinned.',
                  postfreeze_output_policy='Freeze invocation logs, final envelope preflight, real review transition/inspection, review packet, post-review checks, rereview index/launch and final checkpoint are excluded from product manifest and pinned in final-seal.json after creation.',
                  independent_review='Pending fresh separate session; no inherited approval.')
    u.write(u.A/'delivery-manifest.json',manifest)
    artifacts=new+inputs+[u.pin(u.A/'delivery-manifest.json')]
    preflight(artifacts)
    envelope=dict(role='executor',actor=u.CFG['actor'],session_id=u.CFG['session_id'],model=u.CFG['model'],reasoning=u.CFG['reasoning'],
                  configuration_evidence=u.pin(u.A/'configuration-reobservation.json'),
                  summary='IG-2B02-R01/R02 metadata repair: exactly three source-observed component arrays corrected, complete 141-entry ledger, byte-identical canonical snapshots, preserved raw evidence and fresh passing checks; independent rereview pending.',
                  criteria=t['acceptance'],artifacts=artifacts,checks=checks,manifest=u.pin(u.A/'delivery-manifest.json'),
                  handoff=u.pin(u.A/'delivery-handoff.md'),criteria_report=u.pin(u.A/'criteria.json'),
                  checkpoint=cp,write_scope=t['write_scope'],source_observation_scope=list(u.TARGETS),
                  findings_resolution='implemented_pending_independent_review',acceptance_granted=False,
                  measurement=dict(started_utc=u.CFG['records'][0]['observed']['timestamp'],delivery_prepared_utc=u.now(),
                                   input_tokens=None,output_tokens=None,monetary_cost=None,operator_seconds=None,
                                   unknown_reason='Not exposed/reported to executor.'),
                  postfreeze_policy=manifest['postfreeze_output_policy'])
    u.write(u.A/'delivery.json',envelope)
    assert u.load(u.A/'delivery.json')['criteria']==t['acceptance']
    preflight(artifacts)
    print(json.dumps(dict(outcome='frozen',manifest=u.pin(u.A/'delivery-manifest.json'),delivery=u.pin(u.A/'delivery.json'),
                          artifacts=len(artifacts),new_artifacts=len(new),immutable_inputs=len(inputs),metadata_only=len(metadata_only)),indent=2))

def envelope_preflight():
    e=u.load(u.A/'delivery.json');m=u.load(u.A/'delivery-manifest.json');q,t=queue()
    assert q==u.load(u.A/'queue-in-progress.json') and t['status']=='in_progress'
    assert e['criteria']==t['acceptance'] and e['role']=='executor' and e['actor']==u.CFG['actor']
    assert e['model']=='gpt-6.1-sol' and e['reasoning']=='high'
    assert e['artifacts']==m['new_reviewed_artifacts']+m['immutable_inputs_and_old_evidence']+[u.pin(u.A/'delivery-manifest.json')]
    n=preflight(e['artifacts'])
    for x in u.pins_in(e['checks']):u.verify(x)
    assert all(c['exit_code']==0 for c in e['checks'])
    u.write(u.A/'delivery-envelope-preflight.json',dict(outcome='passed_every_final_artifact',checked_artifacts=n,
            delivery=u.pin(u.A/'delivery.json'),manifest=u.pin(u.A/'delivery-manifest.json'),
            rules='Unchanged workflow.safe_path, workflow.denied, actual file, digest and byte size; ordered artifact list exact; all named checks zero.',
            queue_snapshot=u.pin(u.A/'queue-in-progress.json')))
    print('PASS: every final envelope artifact checked through unchanged workflow path/hash rules; ready for one review transition.')

def inspect_review():
    q,t=queue();command=u.load(u.A/'review-transition.command.json');e=u.load(u.A/'delivery.json')
    actual=dict(status=t['status'],latest_event=t['events'][-1],command=command,delivery=u.pin(u.A/'delivery.json'))
    expected=u.load(u.A/'queue-in-progress.json');old=next(x for x in expected['tasks'] if x['id']=='IG-2B02')
    event=t['events'][-1]
    persisted=(t['status']=='review' and event['from']=='in_progress' and event['to']=='review'
               and event['evidence']==u.pin(u.A/'delivery.json')['path'] and event['sha256']==u.sha(u.A/'delivery.json'))
    actual['correct_event_persisted']=persisted
    if persisted:old['status']='review';old['events'].append(event)
    actual['only_authorized_status_event_changed']=persisted and expected==q
    actual['outcome']='passed' if persisted and expected==q and command['exit_code']==0 else 'checkpoint_requires_coordinator'
    u.write(u.A/'review-transition-inspection.json',actual)
    assert actual['outcome']=='passed',actual
    w.validate(q,u.R)
    (u.A/'queue-review.json').write_bytes((u.R/'docs/work/queue.json').read_bytes())
    print(json.dumps(dict(outcome=actual['outcome'],status=t['status'],event=event),indent=2))

def prepare_rereview():
    q,t=queue();assert t['status']=='review' and q==u.load(u.A/'queue-review.json')
    assert u.load(u.A/'review-transition-inspection.json')['outcome']=='passed'
    packet_command=u.load(u.A/'review-packet.command.json');assert packet_command['exit_code']==0
    packet_rel=(u.A/'review-packet.stdout').read_text(encoding='utf-8').strip()
    assert packet_rel.startswith('private/workflow/packets/IG-2B02-')
    packet_dir=w.safe_path(u.R,packet_rel);pm=u.load(packet_dir/'manifest.json')
    assert pm['queue_sha256']==u.sha(u.R/'docs/work/queue.json') and pm['context_sha256']==u.sha(packet_dir/'context.txt')
    for x in pm['files']:u.verify(x)
    assert all(u.load(u.A/(s+'.command.json'))['exit_code']==0 for s in ('post-review-workflow-validate','post-review-diff-check'))
    e=u.load(u.A/'delivery.json')
    current={n:u.pin(u.A/n) for n in CURRENT_NAMES+['delivery.json','delivery-manifest.json','delivery-handoff.md','pre-delivery-checkpoint.json','delivery-envelope-preflight.json','review-transition-inspection.json','configuration-reobservation.json']}
    baseline={n:u.pin(p) for n,p in [('original_delivery',u.D/'delivery-transition-envelope.json'),('original_manifest',u.D/'delivery-manifest.json'),
              ('original_seal',u.D/'final-seal.json'),('original_handoff',u.D/'review-handoff-final.md'),
              ('prior_review',u.V/'review.json'),('prior_review_manifest',u.V/'review-manifest.json'),('prior_review_seal',u.V/'review-seal.json'),
              ('prior_findings',u.V/'findings.json'),('scope',u.P/'repair-scope.json'),('catalogue',u.P/'frozen-base-pins.json'),
              ('coordinator_handoff',u.C/'coordinator-handoff.json')]}
    index=dict(task='IG-2B02',issued_utc=u.now(),repair_actor=u.CFG['actor'],repair_session_id=u.CFG['session_id'],
               repair_actual_model=u.CFG['model'],repair_actual_reasoning=u.CFG['reasoning'],
               current_targets_and_reports=current,immutable_original_inputs=baseline,
               original_metadata_policy='Superseded component descriptions remain historical inputs only; use new current targets for all three corrections.',
               claim_packet=u.load(u.C/'coordinator-handoff.json')['packet'],
               review_packet=dict(directory=packet_rel,manifest=u.pin(packet_dir/'manifest.json'),context=u.pin(packet_dir/'context.txt')),
               queue_snapshot=u.pin(u.A/'queue-review.json'),actual_review_event=t['events'][-1],
               ordered_delivery_artifacts=e['artifacts'],criteria=t['acceptance'],
               final_seal_path=(u.A/'final-seal.json').relative_to(u.R).as_posix(),
               final_seal_hash_policy='Final seal is created after this index and launch and pins both; its real SHA256 is returned separately to operator. The index deliberately does not pin its parent seal, avoiding a hash cycle.',
               reviewer_session_policy='Operator separately authorizes/creates a fresh local independent session, actual gpt-6.1-sol/high proof required. No reviewer identity or decision is invented here.',
               status='review',acceptance_granted=False)
    u.write(u.A/'rereview-input-pins.json',index)
    template=(u.P/'independent-rereview-template.txt').read_text(encoding='utf-8')
    requirements=template.split('Use docs/skills/wgc-review/SKILL.md',1)[1].split('\nEXACT DIRECTORY ALIASES',1)[0]
    launch='IG-2B02-R01/R02 — ISSUED INDEPENDENT REREVIEW HANDOFF\n\n'
    launch+='Communicate in Polish; all repository/private reports in English, explicit UTF-8 without BOM.\n'
    launch+='The repair is frozen and the real queue is review. This handoff does not authorize acceptance, a new chat, or downstream work. The operator separately launches the fresh reviewer.\n\n'
    launch+='Use docs/skills/wgc-review/SKILL.md'+requirements
    launch+='\n\nACTUAL REPAIR IDENTITY\n'+json.dumps({k:index[k] for k in ('repair_actor','repair_session_id','repair_actual_model','repair_actual_reasoning')},indent=2)
    launch+='\nThe fresh reviewer must differ from this repair session, original executor 01a13c20-b7bd-7962-a954-f5841c09831c and prior reviewer 01a13e3c-b2ef-7d90-bdfa-975891f92634.\n'
    launch+='\nACTUAL CURRENT TARGET / REPORT PINS\n'+json.dumps(current,indent=2)
    launch+='\nIMMUTABLE ORIGINAL BASE / REVIEW PINS\n'+json.dumps(baseline,indent=2)
    launch+='\nACTUAL REVIEW EVENT\n'+json.dumps(index['actual_review_event'],indent=2)
    launch+='\nACTUAL NEW REVIEW PACKET\n'+json.dumps(index['review_packet'],indent=2)
    launch+='\nQUEUE SNAPSHOT\n'+json.dumps(index['queue_snapshot'],indent=2)
    launch+='\nCOMPLETE ORDERED REVIEWED LIST AND INPUT INDEX\n'+json.dumps(u.pin(u.A/'rereview-input-pins.json'),indent=2)
    launch+='\nThe ordered_delivery_artifacts field of this pinned index is exactly the new delivery.artifacts list. Preserve the full order in review.json.artifacts.\n'
    launch+='\nREVIEWER-OWNED REPLAY\nThe new replay-repair.py exposes generate(), which reads pinned immutable inputs and returns a name-to-bytes mapping without writes. A reviewer-owned wrapper can import this function and write those returned bytes into two fresh reviewer-owned output directories. Its repair CLI intentionally permits writes only to the repair attempt/direct children; do not invoke that CLI to write into the frozen repair. Retain primary repair logical references when comparing exact bytes.\n'
    launch+='\nFINAL SEAL\n'+index['final_seal_path']+'\n'+index['final_seal_hash_policy']+'\n'
    launch+='\nAll five original acceptance criteria remain unchanged and are in the new packet, delivery.json and pinned index. Review every new report and all 141 regions; source scope and two-retry limits above remain binding. No future reviewer result, identity or hash is asserted.\n'
    with (u.A/'independent-rereview-launch.txt').open('x',encoding='utf-8',newline='\n') as f:f.write(launch)
    print(json.dumps(dict(outcome='actual_rereview_handoff_prepared',launch=u.pin(u.A/'independent-rereview-launch.txt'),index=u.pin(u.A/'rereview-input-pins.json'),packet=index['review_packet']),indent=2))

def seal():
    q,t=queue();assert t['status']=='review' and q==u.load(u.A/'queue-review.json')
    w.validate(q,u.R)
    e=u.load(u.A/'delivery.json');m=u.load(u.A/'delivery-manifest.json');idx=u.load(u.A/'rereview-input-pins.json')
    assert idx['ordered_delivery_artifacts']==e['artifacts']
    count=preflight(e['artifacts']);verify_prepared_pins()
    for x in u.load(u.P/'frozen-base-pins.json')['frozen_pins']:u.verify(x)
    for x in u.pins_in(idx):u.verify(x)
    for name in CURRENT_NAMES:
        for x in u.pins_in(u.load(u.A/name)):
            u.verify(x)
    assert u.load(u.A/'prepare-rereview.command.json')['exit_code']==0
    cfg=u.load(u.A/'configuration-reobservation.json');assert cfg['session_id']==u.CFG['session_id'] and cfg['model']=='gpt-6.1-sol' and cfg['reasoning']=='high'
    cp=checkpoint_snapshot('final-checkpoint.json','stopped_in_review','Operator separately authorizes a fresh independent rereview of exact frozen delivery; no executor continuation.')
    manifest_paths={a['path'] for a in m['new_reviewed_artifacts']}
    post=[u.pin(p) for p in sorted(u.A.rglob('*')) if p.is_file() and p.name not in ('checkpoint.json','final-seal.json') and u.pin(p)['path'] not in manifest_paths]
    preflight(post)
    end=u.now();start=u.CFG['records'][0]['observed']['timestamp']
    elapsed=(datetime.fromisoformat(end)-datetime.fromisoformat(start.replace('Z','+00:00'))).total_seconds()
    result=dict(task='IG-2B02',status='review',actor=u.CFG['actor'],session_id=u.CFG['session_id'],model=u.CFG['model'],reasoning=u.CFG['reasoning'],
                configuration=u.pin(u.A/'configuration.json'),configuration_reobservation=u.pin(u.A/'configuration-reobservation.json'),
                manifest=u.pin(u.A/'delivery-manifest.json'),delivery=u.pin(u.A/'delivery.json'),handoff=u.pin(u.A/'delivery-handoff.md'),
                criteria=u.pin(u.A/'criteria.json'),current_targets={n:u.pin(u.A/n) for n in CURRENT_NAMES},
                rereview_launch=u.pin(u.A/'independent-rereview-launch.txt'),rereview_index=u.pin(u.A/'rereview-input-pins.json'),review_packet=idx['review_packet'],
                review_event=t['events'][-1],queue_snapshot=u.pin(u.A/'queue-review.json'),checkpoint=cp,
                postfreeze_artifacts=post,ordered_delivery_artifact_count=count,all_delivery_artifacts_reverified=True,
                all_4246_frozen_original_references_reverified=True,original_69_pin_table_reverified=True,
                exact_authorized_status_event_only=True,required_checks=u.load(u.A/'required-checks.json'),
                post_review_checks=[u.load(u.A/(n+'.command.json')) for n in ('post-review-workflow-validate','post-review-diff-check')],
                finding_disposition=dict(R01='implemented_pending_independent_review',R02='implemented_pending_independent_review',distinct_targets=3),
                measurement=dict(started_utc=start,ended_utc=end,elapsed_wall_seconds=elapsed,input_tokens=None,output_tokens=None,
                                 monetary_cost=None,operator_seconds=None,unknown_reason='Not exposed/reported to executor.'),
                independent_reviewer=None,independent_reviewer_reason='Not yet separately authorized/created; no reviewer identity invented.',
                independent_review='pending_fresh_separate_session',acceptance_granted=False,semantic_acceptance_granted=False,
                whole_record_source_IG_review='not established',executable_readiness='unverified',downstream_work_started=False,
                defects=dict(findings=2,severity_P2=2,affected_regions=3,implemented_pending_independent_review=2),
                historical_failure_policy='One banner-newline comparison failure retained with original script, logs and changed hypothesis; corrected observation passed. No failed status transition occurred.',
                self_exclusion_policy='Final seal excludes itself. Mutable checkpoint.json is excluded; final-checkpoint.json is the immutable final snapshot. Manifest excludes envelope and all post-freeze outputs, which this seal pins. This invocation writes no subsequent attempt files. Seal command stdout is returned directly to operator, not a future hashed file.',
                seal_command=['./.venv/Scripts/python.exe','-B',(u.A/'delivery-lifecycle.py').relative_to(u.R).as_posix(),'seal'],
                stop='Review reached. Operator may separately authorize fresh independent rereview. No acceptance, done, reviewer creation/message or downstream task.')
    u.write(u.A/'final-seal.json',result)
    print(json.dumps(dict(outcome='stopped_in_review',final_seal=u.pin(u.A/'final-seal.json'),delivery=u.pin(u.A/'delivery.json'),manifest=u.pin(u.A/'delivery-manifest.json'),
                          rereview_launch=u.pin(u.A/'independent-rereview-launch.txt'),rereview_index=u.pin(u.A/'rereview-input-pins.json'),elapsed_wall_seconds=elapsed),indent=2))

if __name__=='__main__':
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('operation',choices=('freeze','envelope-preflight','inspect-review','prepare-rereview','seal'))
    args=parser.parse_args()
    {'freeze':freeze,'envelope-preflight':envelope_preflight,'inspect-review':inspect_review,'prepare-rereview':prepare_rereview,'seal':seal}[args.operation]()
