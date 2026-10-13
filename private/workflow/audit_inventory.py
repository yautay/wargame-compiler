"""Explicit metadata-only audit of original manifests against relocation hashes."""
from collections import Counter, defaultdict
import json
from pathlib import Path

root=Path(__file__).resolve().parents[2]
def read(rel): return json.loads((root/rel).read_text(encoding='utf-8-sig'))
m=read('private/workflow/relocation.json')
lookup={e['old_path']:e for e in m['entries']}
poc=read('private/archive/poc-2026-10-11/manifest.json')['entries']
poc_orig={e['original_path']:e['archive_path'] for e in poc}
checks=[]
def check(name,entries):
    mismatches=[]; count=0
    for path,size,sha in entries:
        count+=1
        actual=lookup.get(path)
        if actual is None or actual['bytes']!=size or actual['sha256'].lower()!=sha.lower():
            mismatches.append(path)
    checks.append({'manifest':name,'entries':count,'mismatches':mismatches})
check('private/archive/poc-2026-10-11/manifest.json',[(e['archive_path'],e['bytes'],e['sha256']) for e in poc])
pre=read('private/archive/2026-10-07-pre-poc/manifest.json')['files']
check('pre-poc payload', [('private/archive/2026-10-07-pre-poc/payload/'+e['path'],e['size'],e['sha256']) for e in pre])
check('pre-poc restore-check', [('private/archive/2026-10-07-pre-poc/restore-check/'+e['path'],e['size'],e['sha256']) for e in pre])
check('restore-cli-check', [('private/archive/restore-cli-check-2026-10-07/'+e['path'],e['size'],e['sha256']) for e in pre])
for path in ['archive/legacy-2026-10-07/movement-map.json','private/archive/2026-10-07-pre-poc/movement-map.json']:
    entries=read(path)
    check(path,[(e['destination'] if e['destination'] in lookup else poc_orig.get(e['destination'],e['destination']),e['size'],e['sha256']) for e in entries])
saved=read('archive/planning-before-sol-2026-10-11/manifest.json')['entries']
check('planning pre-edit snapshot',[(e['snapshot_path'],e['bytes'],e['sha256']) for e in saved])
counts=Counter((e['bytes'],e['sha256']) for e in m['entries'])
groups=defaultdict(lambda: {'files':0,'bytes':0,'single_copy_hashes':0})
for e in m['entries']:
    key=next(r for r in m['roots'] if e['old_path']==r or e['old_path'].startswith(r+'/'))
    groups[key]['files']+=1; groups[key]['bytes']+=e['bytes']
    groups[key]['single_copy_hashes']+=counts[e['bytes'],e['sha256']]==1
report={'result':'passed' if not any(c['mismatches'] for c in checks) else 'mismatch',
        'files':len(m['entries']),'bytes':sum(e['bytes'] for e in m['entries']),
        'distinct_byte_hashes':len(counts),'single_copy_files':sum(n==1 for n in counts.values()),
        'roots':dict(groups),'original_manifest_checks':checks,
        'meaning':'Byte duplicates are identified only for inventory; no deduplication or historical content reading.',
        'migration':'not performed; external writes unavailable'}
variants=[]
for item in read('archive/legacy-2026-10-07/movement-map.json'):
    path=item['destination']; actual=lookup.get(path)
    if actual and actual['sha256']!=item['sha256']:
        preserved='private/archive/2026-10-07-pre-poc/payload/'+item['path']
        variants.append({'path':path,'expected_sha256':item['sha256'],'current_sha256':actual['sha256'],
                         'expected_bytes':item['size'],'current_bytes':actual['bytes'],
                         'original_preserved_at':preserved,
                         'original_verified':lookup[preserved]['sha256']==item['sha256']})
report['legacy_variants']=variants
report['interpretation']='Eight pre-existing legacy variants preserved alongside byte-correct originals; no historical repair or normalization performed.'
(root/'private/workflow/archive-audit.json').write_text(json.dumps(report,indent=2)+'\n',encoding='utf-8')
print(json.dumps({k:report[k] for k in ['result','files','bytes','distinct_byte_hashes','single_copy_files','legacy_variants']},indent=2))
