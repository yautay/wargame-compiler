from ops import *
q=load('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-2B02');assert t['status']=='in_progress' and len(t['events'])==2 and t['events'][-1]['evidence']==AR+'/claim.json' and t['events'][-1]['sha256']==pin(A/'claim.json')['sha256']
claim_event=t['events'].pop();t['status']='ready';raw=(json.dumps(q,ensure_ascii=False,indent=2)+'\n').replace('\n','\r\n').encode('utf-8');expected=load(PK+'/manifest.json')['queue_sha256'];actual=hashlib.sha256(raw).hexdigest();assert actual==expected,(actual,expected)
write('queue-mutation-audit.json',{'outcome':'passed','preclaim_queue_sha256':expected,'reconstructed_preclaim_sha256':actual,'policy':'Current queue differs from exact supplied packet only by this executor authorized ready -> in_progress status/event. No structural or downstream edits.','claim_event':claim_event,'current_queue':pin('docs/work/queue.json'),'actual_claim':pin(A/'claim.json')})
print('QUEUE ONLY AUTHORIZED CLAIM CHANGE VERIFIED')
