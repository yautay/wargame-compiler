"""Embed the exact pinned WGU structural schema in the owned importer path."""
from pathlib import Path
import hashlib,json
schema=Path(__file__).parent/'pinned-wgu-schema.json'
raw=schema.read_bytes()
assert hashlib.sha256(raw).hexdigest()=='0a93858ed3e0d99382ea962350e3b2994fab90b872a8b86584519b5a9e33a551'
literal=repr(json.dumps(json.loads(raw),ensure_ascii=False,separators=(',',':')))
p=Path('src/wgc/wgu_adapter/importer.py');s=p.read_text()
marker='WGU_SCHEMA = None  # Replaced from the exact preserved schema by the repair build.'
assert s.count(marker)==1
with p.open('w',encoding='utf-8',newline='\n') as f:f.write(s.replace(marker,'WGU_SCHEMA = json.loads('+literal+')'))
print('Exact pinned structural schema embedded; no neighboring runtime reads')
