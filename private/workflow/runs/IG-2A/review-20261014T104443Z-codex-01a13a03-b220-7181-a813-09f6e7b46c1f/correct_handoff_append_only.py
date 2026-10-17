from support import *

# The first successful freeze and every file it contains are immutable. Append only.
for entry in read(RUN/'review-manifest.json')['artifacts']:
    assert digest(ROOT/entry['path'])==entry['sha256'],entry['path']
old_seal=pin(RUN/'final-seal.json');old_handoff=pin(RUN/'coordinator-handoff.json')
old_review=pin(RUN/'review.json')
assert read(RUN/'coordinator-handoff.json')['review']['sha256']!=old_review['sha256']
delivery=read(REPAIR/'delivery.json')['artifacts'];members=read(REPAIR/'delivery-manifest.json')['artifacts']
assert len(delivery)==273 and len(members)==272
assert [x for x in delivery if x['path'] not in {e['path'] for e in members}]==[pin(REPAIR/'delivery-manifest.json')]
for e in delivery:assert digest(ROOT/e['path'])==e['sha256']
error=read(RUN/'clarify-delivery-count.json');assert error['exit_code']==1
note={'actor':read(RUN/'configuration.json')['actor'],'task':'IG-2A','role':'reviewer','original_freeze':old_seal,'original_handoff':old_handoff,'current_original_review':old_review,'cause':'Reviewer count clarification updated review.json before report update raised UnicodeDecodeError due missing explicit UTF-8 on Windows. Reviewer mistakenly allowed the dependent freeze to run after this failed update, leaving the frozen original handoff with its previous review hash.','failed_command':error,'freeze_guard_count_explanation':'273 delivery artifacts = 272 self-excluding manifest members plus the manifest itself; no operator pin mismatch.','correction':'Append-only new report-final.md, review-final.json, coordinator-handoff-final.json and final-seal-corrected.json replace the handoff metadata. Preserve all first-freeze files and its manifest/seal byte-for-byte. No product, queue, expected hashes or probe expectations changed.','technical_outcome_unchanged':'PASS','reviewer_implementation_error':True,'source_or_product_error':False,'recorded_utc':utc()}
write('append-only-handoff-correction.json',note)
report=(RUN/'report.md').read_text(encoding='utf-8')
report=report.replace('All 273 delivery artifacts, sealed post-freeze/governance artifacts','All 273 delivery artifacts (272 self-excluding manifest members plus the manifest itself), sealed post-freeze/governance artifacts')
report+='''

## Append-only finalization correction

The first reviewer freeze guard compared 272 self-excluding delivery-manifest members with the 273 delivery entries and failed. Independent set comparison confirmed that the extra delivery entry is exactly the manifest itself, with the expected operator hash. All 273 entries were explicitly verified; no expected hash changed.

The reviewer's count-clarification helper subsequently changed review.json, then failed while reading report.md with the Windows default cp1252 codec. The reviewer incorrectly ran the dependent freeze despite this helper failure. As a result, the first frozen coordinator-handoff.json references the pre-update review hash. This is a reviewer handoff metadata error, not a product validation result. Both failed commands and the first successful seal remain intact.

This final report, review-final.json, coordinator-handoff-final.json, review-final-manifest.json and final-seal-corrected.json are append-only replacements for coordinator consumption. The original report/review/handoff/manifest/seal and every first-manifest artifact remain byte-identical. The corrected handoff pins the exact current final review and final report. All 273 delivery pins and original reviewer manifest pins were verified again. Technical outcome remains PASS; the final coordinator handoff is the suffixed final file. No product, queue, input pin or expected result changed. The corrected seal records the final end UTC and elapsed session wall time, superseding only the earlier finalization boundary.
'''
final_report=RUN/'report-final.md';final_report.write_text(report,encoding='utf-8')
review=read(RUN/'review.json')
review['artifacts']=[pin(final_report) if a['path']==(RUN/'report.md').relative_to(ROOT).as_posix() else a for a in review['artifacts']]
review['artifacts'].extend([pin(RUN/'delivery-artifact-verification.json'),pin(RUN/'append-only-handoff-correction.json')])
review['append_only_finalization_correction']=pin(RUN/'append-only-handoff-correction.json')
write('review-final.json',review)
handoff=read(RUN/'coordinator-handoff.json');handoff['review']=pin(RUN/'review-final.json');handoff['report']=pin(final_report)
handoff['supersedes_metadata_handoff']=old_handoff
handoff['correction_evidence']=pin(RUN/'append-only-handoff-correction.json')
write('coordinator-handoff-final.json',handoff)
# Verify every artifact and reference before constructing the replacement seal.
for a in review['artifacts']:assert digest(ROOT/a['path'])==a['sha256'],a['path']
for key in ['review','report','delivery','delivery_manifest','delivery_final_seal']:
    a=handoff[key];assert digest(ROOT/a['path'])==a['sha256'],a['path']
for entry in read(RUN/'review-manifest.json')['artifacts']:
    assert digest(ROOT/entry['path'])==entry['sha256'],entry['path']
files=[pin(p) for p in sorted(RUN.rglob('*')) if p.is_file()]
assert not (RUN/'review-final-manifest.json').exists() and not (RUN/'final-seal-corrected.json').exists()
write('review-final-manifest.json',{'format':'wgc-independent-review-manifest-1','task':'IG-2A','actor':review['actor'],'outcome':'PASS','artifacts':files,'artifact_count':len(files),'reviewed_delivery_artifacts':delivery,'original_freeze_preserved':old_seal,'exclusions':['This self-excluding final manifest and the later final-seal-corrected.json only. All operational scratch and first-freeze artifacts included.'],'created_utc':utc()})
for a in files:assert digest(ROOT/a['path'])==a['sha256'],a['path']
ended=utc();started=read(RUN/'configuration.json')['started_utc']
new_seal=read(RUN/'final-seal.json')
new_seal.update(manifest=pin(RUN/'review-final-manifest.json'),review=pin(RUN/'review-final.json'),handoff=pin(RUN/'coordinator-handoff-final.json'),report=pin(final_report),ended_utc=ended,wall_seconds=(datetime.fromisoformat(ended)-datetime.fromisoformat(started.replace('Z','+00:00'))).total_seconds(),all_manifest_artifacts_verified=len(files),supersedes_metadata_freeze=old_seal,append_only_correction=pin(RUN/'append-only-handoff-correction.json'),exclusions='final-seal-corrected.json cannot hash itself; review-final-manifest.json hashes every other reviewer file, including original freeze and operational scratch. Use the corrected seal and final handoff for coordinator review.')
write('final-seal-corrected.json',new_seal)
print(json.dumps({'outcome':'PASS','manifest':pin(RUN/'review-final-manifest.json'),'final_seal':pin(RUN/'final-seal-corrected.json'),'handoff':pin(RUN/'coordinator-handoff-final.json'),'review_files':len(files),'wall_seconds':new_seal['wall_seconds']},indent=2))
