from prepare import *
tool=read(f'{REL}/toolchain.json')
sys.path[:0]=tool['process_pythonpath'].split(';')
os.environ['PATH']=tool['process_path_prefix']+';'+os.environ['PATH']
import pdfplumber
from PIL import Image
(RUN/'pages').mkdir(exist_ok=False)
start=datetime.now(timezone.utc)
with pdfplumber.open(ROOT/f'{SOURCE}/rulebook.pdf') as pdf:
 for number in range(1,5):
  page=pdf.pages[number-1]
  (RUN/f'pages/page-{number:02}.txt').write_text(page.extract_text(layout=False),encoding='utf-8')
  words=page.extract_words(extra_attrs=['fontname','size'])
  write(f'{REL}/pages/page-{number:02}-words.json',words)
  print('PAGE',number)
  for side,(x0,x1) in enumerate([(0,306),(306,612)]):
   rows={}
   for w in words:
    if x0 <= (w['x0']+w['x1'])/2 < x1:
     rows.setdefault(round(w['top'],1),[]).append(w)
   for y,ws in sorted(rows.items()):
    ws.sort(key=lambda w:w['x0']); print(side,y,round(min(w['x0'] for w in ws),1),round(max(w['bottom'] for w in ws),1),' '.join(w['text'] for w in ws))
 r=None
r=run('render-pages',[tool['native']['pdftoppm']['path'],'-f','1','-l','4','-r','144','-cropbox','-png',str(ROOT/f'{SOURCE}/rulebook.pdf'),str(RUN/'pages/original')]); assert r.returncode==0
write(f'{REL}/page-access.json',{'content_pages':[1,2,3,4],'context_page_5_accessed':False,'other_pages':'Structural count/geometry only','started_utc':start.isoformat(),'ended_utc':datetime.now(timezone.utc).isoformat()})
