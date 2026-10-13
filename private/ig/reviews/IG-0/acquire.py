import json, hashlib, urllib.request, concurrent.futures
from pathlib import Path
from pypdf import PdfReader
root=Path('private/ig/reviews/IG-0')
urls={
'tlnb':'https://cdn.shopify.com/s/files/1/0443/6423/4910/files/TLNB_SeriesRules-7.38-2.pdf?v=1741466415',
'nab':'https://cdn.shopify.com/s/files/1/0443/6423/4910/files/nab_exclusive_rules_update_kit__24k.pdf?v=1601499015',
'lastdays':'https://cdn.shopify.com/s/files/1/0443/6423/4910/files/ldga_1.12paged.pdf?v=1603458711',
'sevendays':'https://cdn.shopify.com/s/files/1/0443/6423/4910/files/7D09-Rules_3.27.pdf?v=1603456254',
'gcacw':'https://mmpgamers.com/support/gcacw/GCACW_Series_Rules_1.6.pdf',
'gcacw-tables':'https://mmpgamers.com/support/gcacw/GCACW_Charts_Tables_1.6.pdf',
'rtg2':'https://mmpgamers.com/support/gcacw/RTG2_Rules.pdf',
 'tlnb-tables':'https://cdn.shopify.com/s/files/1/0443/6423/4910/files/COMBAT_TABLES.pdf?v=1603420083'
}
def fetch(item):
 k,u=item
 try:
  data=urllib.request.urlopen(u,timeout=30).read()
  assert data.startswith(b'%PDF')
  p=root/'sources'/f'{k}.pdf'; p.write_bytes(data)
  reader=PdfReader(p)
  for i,page in enumerate(reader.pages):
   (root/'sources'/f'{k}-p{i+1:03}.txt').write_text(page.extract_text(),encoding='utf-8')
  return dict(id=k,url=u,path=str(p),sha256=hashlib.sha256(data).hexdigest(),bytes=len(data),pages=len(reader.pages),read_status='downloaded_not_fully_read')
 except Exception as e: return dict(id=k,url=u,error=str(e))
with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: result=list(pool.map(fetch,urls.items()))
m=json.loads(Path('private/archive/poc-2026-10-11/manifest.json').read_text(encoding='utf-8-sig'))
e=next(e for e in m['entries'] if e['original_path']=='private/poc/spqr-chapter9/source/original-pdf-20261008-01.pdf')
p=Path(e['archive_path']); assert hashlib.sha256(p.read_bytes()).hexdigest()==e['sha256']
reader=PdfReader(p)
for n in [1,11,12,13,15,26,27,37,38,41]:
 (root/'sources'/f'spqr-p{n:03}.txt').write_text(reader.pages[n-1].extract_text(),encoding='utf-8')
result.append(dict(id='spqr',path=str(p),sha256=e['sha256'],pages=len(reader.pages),resolved_via_manifest=True))
(root/'sources-manifest.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
