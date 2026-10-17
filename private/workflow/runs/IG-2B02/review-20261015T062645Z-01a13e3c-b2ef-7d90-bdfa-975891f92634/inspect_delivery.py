from review_driver import *
ledger=load(D/'region-ledger-final.json')
for n,row in enumerate(ledger['regions'],1):
    r=row['region']
    print(f"{n:03} p{row['pdf_page']} {r['key']} {r['box']} :: {row['label']} :: {row['components']}")
print('SCRIPTS')
for p in load(D/'delivery-manifest.json')['new_reviewed_artifacts']:
    if p['path'].endswith('.py'):print(p['path'].rsplit('/',1)[-1])
print('GEOMETRY KEYS',load(D/'geometric-gaps.json').keys())
print('LINKS')
rs={r['id']:r['key'] for r in load(D/'final-verified/inventory.json')['regions']}
for link in load(D/'continuations.json')['added_links']:print(link['kind'],rs[link['from']],'->',rs[link['to']],link['reason'])
