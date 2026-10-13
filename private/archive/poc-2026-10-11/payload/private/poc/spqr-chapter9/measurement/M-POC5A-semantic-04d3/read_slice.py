"""Display frozen source child scopes and original mapped fields, never extract anew."""
from pathlib import Path
import json,sys
P=Path('private/poc/spqr-chapter9');C=json.loads((P/'reviews/semantic-01/checklist.json').read_bytes());plan=json.loads((P/'measurement/M-POC5A-semantic-04d1/scope-plan.json').read_bytes());ids=plan['parts'][2]['inventory_ids'];seen=set()
def compact(v):
    if isinstance(v,dict):return {k:compact(x) for k,x in v.items() if k!='evidence_ids'}
    if isinstance(v,list):return [compact(x) for x in v]
    return v
for i in range(int(sys.argv[1]),int(sys.argv[2])):
    iid=ids[i];x=next(z for z in C['inventory'] if z['id']==iid);f=x['frozen_item'];print('\nITEM',i,iid,x['type'],'EXPECT',x['expectation_ids'])
    print('SOURCE',f.get('source_transcription') or '\n'.join(e.get('transcription','[Graphic source: inspect supplied image and original inventory observation]') for e in f['evidence']))
    if x['type'] in ['diagram','counter_illustration','table','table_row','caption']:print('GRAPHIC INVENTORY',json.dumps(f,ensure_ascii=False))
    for run in C['responses']:
        for rid in x['runs'][run]['output_record_ids']:
            if (run,rid) in seen:print(run,rid,'same original mapped record printed above; child source comparison required');continue
            seen.add((run,rid));rec=C['output_records'][run][rid]['original_record'];print(run,json.dumps(compact(rec) if len(sys.argv)>3 else rec,ensure_ascii=False))
