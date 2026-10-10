"""Immutable context-response receipt; independent evidence kept apart from claims."""
from pathlib import Path
import datetime,hashlib,json,subprocess
ROOT=Path.cwd();P=ROOT/'private/poc/spqr-chapter9';M=P/'measurement/M-POC4B-context-01'
T=P/'transfer/context-v1';R=P/'runs/context-01'
def sha(b):return hashlib.sha256(b).hexdigest()
def desc(x):
    b=x.read_bytes();return dict(path=x.relative_to(ROOT).as_posix(),bytes=len(b),sha256=sha(b))
def load(x):return json.loads(x.read_bytes())
def save(x,obj):
    assert not x.exists(),x
    x.write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
before=[]
for folder in ['runs/first-001','proposals/first-001','reports/first-001','inputs/v1',
    'transfer/first-v1','evaluation/eval-v1','source','prompts','formats','context/pass-01',
    'transfer/context-v1','evaluation/M-POC4A-review-001','measurement/M-POC3-first-001',
    'measurement/M-POC4A-pass-01','measurement/M-POC4A-review-001']:
    before += [desc(x) for x in sorted((P/folder).rglob('*')) if x.is_file() and '__pycache__' not in x.parts]
before.append(desc(P/'measurement/sessions.jsonl'))
save(M/'protected-before.json',before)
manifest=load(T/'context/pass-01/manifest.json');freeze=load(P/'context/pass-01/freeze-v1.json')
assert desc(T/'context/pass-01/manifest.json')==freeze['transfer_manifest']
for a in manifest['artifacts']:
    b=(T/a['path']).read_bytes();assert len(b)==a['bytes'] and sha(b)==a['sha256'],a['path']
eval_manifest=load(P/'evaluation/eval-v1/manifest.json')
for a in eval_manifest['artifacts']:assert desc(ROOT/a['path'])==a
baseline=load(P/'reports/first-001/manifest.json');closure=load(P/'reports/first-001/closure.json')
assert desc(P/'reports/first-001/manifest.json')==closure['report_manifest']
for a in baseline['artifacts']:assert desc(ROOT/a['path'])==a
assert (T/'parent/first-001.json').read_bytes()==(P/'runs/first-001/first-001.json').read_bytes()
source=T/'context-01.json';raw=source.read_bytes()
assert sha(raw)=='95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b'
assert not R.exists();R.mkdir()
(R/'response.raw.txt').write_bytes(raw)
d=json.loads(raw);assert d['run_id']=='context-01'
history=load(M/'extractor-thread-snapshot.json');turn=history['turns'][0]
commands=[i for i in turn['items'] if i['type']=='commandExecution']
observed=[dict(id=i['id'],command=i['command'],cwd=i.get('cwd'),status=i.get('status'),exit_code=i.get('exitCode')) for i in commands]
snapshot=desc(M/'extractor-thread-snapshot.json')
clock=lambda sec:datetime.datetime.fromtimestamp(sec,datetime.timezone.utc).isoformat()
record=dict(run_id='context-01',card='M-POC4B',phase='receipt_of_existing_manual_response',
    registered_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),timezone='Europe/Warsaw',
    response=dict(original=desc(source),preserved=desc(R/'response.raw.txt'),byte_identical=True,
        original_save_method='Transcript contains a local PowerShell write; exact bytes verified at receipt. Filesystem timestamps not used.'),
    parent_response=desc(P/'runs/first-001/first-001.json'),input_manifest=desc(T/'context/pass-01/manifest.json'),
    original_input_manifest=desc(P/'inputs/v1/manifest.json'),freeze=desc(P/'context/pass-01/freeze-v1.json'),
    prompt=desc(T/'prompts/context-v1.txt'),actual_prompt_evidence='Transcript shows allowlisted prompt read; user kickoff preserved in the snapshot.',
    assessment_id='eval-v1',evaluation_manifest=desc(P/'evaluation/eval-v1/manifest.json'),
    input_integrity=dict(context_artifacts=41,original_artifacts=32,allowlisted_input_files=42,all_match=True,
        verification_scope='Independent current byte checks; extraction-time hash statements compared as claims, not accepted wholesale.'),
    session_evidence=dict(snapshot=snapshot,thread_id='01a12690-583e-77b3-a182-1c83498a26ba',
        turn_id=turn['id'],snapshot_provider='Codex app read_thread',commands_observed=len(commands),
        independent_scope_deviation=True,evidence_commands=observed[:3],
        scope='Attempted absent root transfer-list read, root entry-name listing and path search outside allowlist are observed. Names/path metadata access is not itself proof of reading evaluation content.',
        assessment_content_read_observed=False,assessment_exposure='unknown',clean_context_verified=False,
        no_proven_contamination=True,no_proven_full_isolation=True,
        limitations='Transcript outputs can be truncated; prior context/UI selector and all implicit environment access are not independently established.'),
    extraction_configuration=dict(application='Codex task in desktop app',application_evidence='App thread metadata and command history',
        actual_model_visible_name='unknown',reasoning_level='unknown',configuration_selectors='unknown'),
    timing=dict(turn_started_at_utc=clock(turn['startedAt']),turn_completed_at_utc=clock(turn['completedAt']),
        turn_calendar_elapsed_seconds=turn['durationMs']/1000,
        actual_extraction_start_end='unknown',user_active_time='unknown',model_active_time='unknown',
        tokens='unknown',price='unknown',active_budget_remaining='unknown',time_budget_compliance='unknown',
        limitation='App turn timings independently recorded; not active user/model/inference time. Receipt is not a repeat extraction.'),
    extractor_self_report=d.get('provenance'),self_report_policy='Preserved as claims; not independent evidence of blind session, selected model, timing, source validity or meaning.',
    semantic_acceptance='not_performed',scope_selection_acceptance='Previously owner-approved bounded source only',
    counters=dict(context_response_rounds_total=1,new_inference_responses_in_receipt=0,corrective_responses=0),
    not_performed=['new extraction','response edits','correction','pass-02','M-POC5'],
    receipt_owner_instruction='Current owner says the other session performed the response and instructs continuing the M-POC4B evaluation.')
save(R/'run.json',record)
evidence='''M-POC4B / context-01 receipt, 2026-10-10 Europe/Warsaw.
Original local output: transfer/context-v1/context-01.json. The entire 712014-byte UTF-8 JSON file is preserved as response.raw.txt, without any edit or wrapper removal.
Independent checks: SHA-256 95b2254026aef3ba7c22a69917f8758d9f1bafa777c4d906f820bfeaca263c9b; context manifest SHA-256 1140a43519ae60646ea783bb24ec4dacc2f608e88d80efd83a206427aa45eff4; all 41 manifest artifacts/42 input files verified; parent and frozen eval-v1/baseline reports unchanged.
Independent app transcript: measurement/M-POC4B-context-01/extractor-thread-snapshot.json. The user kickoff, completed turn and commands are preserved. Initial metadata discovery in the repository root is independently observed. Root names/path enumeration violated the no-parent-directory rule; this does not prove evaluation-content exposure. No such content read observed in available transcript; full clean context and assessment exposure remain unknown. Do not declare contamination or full isolation from this record alone.
App turn start/end and wall-clock elapsed are independent turn metadata, not active user/model time. Exact selected model/reasoning, active budget, tokens and price remain unknown.
The entire extractor provenance is retained only as self-report in run.json and raw answer. This receipt does not confer semantic acceptance and does not repeat extraction or perform a correction.
'''
(R/'session-evidence.txt').write_text(evidence,encoding='utf-8')
save(M/'receipt-integrity.json',dict(response=desc(R/'response.raw.txt'),run=desc(R/'run.json'),
    snapshot=snapshot,context_inputs_verified=41,eval_artifacts_verified=7,baseline_report_artifacts_verified=10,
    all_match=True,protected_files=len(before),session_evidence=desc(R/'session-evidence.txt')))
print('Receipt preserved',len(raw),'bytes; independent transcript commands',len(commands))
