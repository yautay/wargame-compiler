import json,hashlib,subprocess
from pathlib import Path
import pdfplumber
ROOT=Path(__file__).parent
PDF=Path('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf')
assert hashlib.sha256(PDF.read_bytes()).hexdigest()=='e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
OUT=ROOT/'originals';OUT.mkdir(exist_ok=False)
records=[]
with pdfplumber.open(PDF) as doc:
 for n in (29,30,31,32,33):
  page=doc.pages[n-1]
  args=['pdftoppm','-f',str(n),'-l',str(n),'-singlefile','-r','144','-png']
  if n==33:
   page=page.crop((45,50,306,80),strict=True)
   args+=['-x','90','-y','100','-W','522','-H','60']
  text=page.extract_text(x_tolerance=3,y_tolerance=3,layout=False) or ''
  prefix=OUT/f'page-{n}'
  prefix.with_suffix('.txt').write_text(text,encoding='utf-8')
  subprocess.run(args+[str(PDF),str(prefix)],check=True,capture_output=True)
  records.append({'page':n,'box':[45,50,306,80] if n==33 else [0,0,612,792],'png_sha256':hashlib.sha256(prefix.with_suffix('.png').read_bytes()).hexdigest()})
(ROOT/'source-access.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print(json.dumps(records))
