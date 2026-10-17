from support import *
delivery=read(REPAIR/'delivery.json')['artifacts'];members=read(REPAIR/'delivery-manifest.json')['artifacts']
assert len(delivery)==273 and len(members)==272
extra=[p for p in delivery if p['path'] not in {e['path'] for e in members}]
assert extra==[pin(REPAIR/'delivery-manifest.json')]
for p in delivery:assert digest(ROOT/p['path'])==p['sha256']
write('delivery-artifact-verification.json',{'delivery_count':273,'manifest_members':272,'additional_delivery_artifact':extra[0],'explanation':'Delivery has all 272 manifest member artifacts plus the manifest itself. A manifest cannot hash itself. All 273 delivery entries verified explicitly; existing operator expected hashes unchanged.','artifacts':delivery,'all_match':True})
write('freeze-01-failure.json',{'command':'.venv/Scripts/python.exe '+(RUN/'freeze_review.py').relative_to(ROOT).as_posix(),'exit_code':1,'tool_elapsed_wall_seconds':0.9484337,'started_utc':None,'ended_utc':None,'error':'AssertionError at len(verified)==273 when reading 272 self-excluding manifest members','resolution':'Use all 273 entries in frozen delivery.json, including the manifest. Independent set comparison verified the difference is exactly the manifest itself, with the expected operator SHA256. No expected hash changed.','manifest_or_seal_written':False})
# Repair only reviewer metadata/report, before any successful freeze. No product edit.
review=read(RUN/'review.json')
review['artifacts'].insert(272,pin(REPAIR/'delivery-manifest.json'))
write('review.json',review)
report=(RUN/'report.md').read_text()
report=report.replace('All 273 delivery artifacts, sealed post-freeze/governance artifacts','All 273 delivery artifacts (272 manifest members plus the manifest itself), sealed post-freeze/governance artifacts')
report=report.replace('All substantive validation commands passed.', 'All substantive validation commands passed. The first reviewer freeze guard failed because it counted the 272 self-excluding manifest members as the 273 delivery artifacts; an exact set comparison confirmed that delivery.json adds only the manifest itself. All 273 entries were then explicitly verified without changing expected hashes. `freeze-01-failure.json` preserves the failed command and observed elapsed time; no manifest/seal had been written.')
(RUN/'report.md').write_text(report,encoding='utf-8')
# Updated report pin in review evidence and updated review/report handoff pins.
review=read(RUN/'review.json')
review['artifacts']=[pin(RUN/'report.md') if e['path']==(RUN/'report.md').relative_to(ROOT).as_posix() else e for e in review['artifacts']]
write('review.json',review)
handoff=read(RUN/'coordinator-handoff.json');handoff['review']=pin(RUN/'review.json');handoff['report']=pin(RUN/'report.md');write('coordinator-handoff.json',handoff)
print('273 exact delivery entries match: 272 members plus manifest; report pins updated')
