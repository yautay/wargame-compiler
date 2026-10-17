"""Arrange every exact region PNG back into its source-page position for QA."""
from PIL import Image
import pathlib,json,sys,math
r=pathlib.Path(__file__).parent
plan=json.loads((r/'authored/partition-plan.json').read_text())['regions']
dest=r/'evidence-mosaics';dest.mkdir(exist_ok=True)
for n in map(int,sys.argv[1:]):
 out=dest/f'page-{n:02d}.png';assert not out.exists()
 im=Image.new('RGB',(1530,1980),'white')
 for row in [x for x in plan if x['page']==n]:
  part=Image.open(r/'final-verified/evidence'/row['region_id'].split(':')[1]/'image.png').convert('RGB')
  b=row['box'];x,y=math.floor(b[0]*1530/1000000),math.floor(b[1]*1980/1000000)
  if row['kind']=='diagram':part=part.resize((math.ceil((b[2]-b[0])*1530/1000000),math.ceil((b[3]-b[1])*1980/1000000)),Image.Resampling.LANCZOS)
  im.paste(part,(x,y))
 im.save(out);print(out)
