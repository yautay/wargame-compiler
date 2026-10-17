from ops import *
import pdfplumber
s=load(P+'/scope.json');base=load(s['baseline']['path'])
q=load('docs/work/queue.json');t=next(t for t in q['tasks'] if t['id']=='IG-2B02');assert t['status']=='in_progress' and t['events'][-1]['sha256']==pin(A/'claim.json')['sha256']
write('claim-event-verification.json',{'status':t['status'],'event':t['events'][-1],'actual_claim_pin':pin(A/'claim.json'),'verified_utc':now()})
assert pin(s['baseline']['path'])==s['baseline'] and pin(s['registry']['path'])==s['registry']
(A/'inspection').mkdir(exist_ok=False)
c=run('render-originals',[POP+'/pdftoppm.EXE','-f','5','-l','8','-cropbox','-r','144','-png',str(R/base['source']['pdf']['path']),str(A/'inspection/original')]);assert c['exit_code']==0
with pdfplumber.open(R/base['source']['pdf']['path']) as pdf:
 for n in (5,6,7,8):
  page=pdf.pages[n-1]
  (A/f'inspection/p{n}-raw.txt').write_text(page.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or '',encoding='utf-8',newline='\n')
  lines=[]
  for col,box in [('left',(0,0,page.width/2,page.height)),('right',(page.width/2,0,page.width,page.height))]:
   for line in page.crop(box).extract_text_lines(layout=False,strip=True,return_chars=False):lines.append({'column':col,**line})
  write(f'inspection/p{n}-lines.json',{'width':page.width,'height':page.height,'lines':lines})
write('context-access.json',{'page_4':{'need':'Compare accepted Triarii fragment with newly observed physical-page-5 continuation','allowed_region':s['continuation_context']['page_4']['region'],'evidence':s['continuation_context']['page_4']['evidence'],'access_policy':s['continuation_context']['page_4']['access']},'page_9':{'accessed':False,'need':None,'box':None},'unassigned_content_access':'No other content access'})
checkpoint('originals',['Preflight and exclusive claim','Original pages 5-8 rendered at 144 DPI; raw local extraction retained'],'Inspect each original assigned page and manually author explicit region specifications')
print('ORIGINAL OBSERVATION FILES READY')
