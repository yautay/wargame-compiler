from pathlib import Path
import hashlib,json
root=Path('private/ig/reviews/IG-0')
manifest=json.loads((root/'sources-manifest.json').read_text(encoding='utf-8'))
for item in manifest:
 p=Path(item['path']); actual=hashlib.sha256(p.read_bytes()).hexdigest()
 assert actual==item['sha256'],p
 item['acquisition_date_local']='2026-10-11'
 item['full_document_read']=False
 item['read_scope_ref']='evidence-and-examples.md'
 if item['id']!='spqr': item['read_status']='selected_fragments_reviewed'
(root/'sources-manifest.json').write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
files=[Path(p) for p in ['docs/reviews/IG-0-critical-review.md','docs/IG-DATA-MODEL.md','docs/IG-MECHANICS-PROFILES.md','docs/IG-PLAN.md','docs/STATUS.md','docs/HANDOFF.md','docs/ROADMAP.md','docs/work/tasks/IG-0.md']]
files += [root/'evidence-and-examples.md']
for p in files:
 for i,line in enumerate(p.read_text(encoding='utf-8-sig').splitlines(),1):
  assert line==line.rstrip(),(str(p),i,'trailing whitespace')
assert (root/'evidence-and-examples.md').read_text(encoding='utf-8').count('```yaml')==7
print('9 source hashes verified; 9 authored/edited Markdown files whitespace clean; 7 representation sketches')
