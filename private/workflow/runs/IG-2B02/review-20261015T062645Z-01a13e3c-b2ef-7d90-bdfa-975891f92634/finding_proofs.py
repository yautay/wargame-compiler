from review_driver import *
from PIL import Image
from math import floor,ceil
ledger=load(D/'region-ledger-final.json')['regions']
for index in (6,25,29):
    row=ledger[index-1];b=row['region']['box']
    with Image.open(R/f"originals/original-{row['pdf_page']:02}.png") as original:
        crop=original.crop((floor(b[0]*1224/1e6),floor(b[1]*1584/1e6),ceil(b[2]*1224/1e6),ceil(b[3]*1584/1e6)))
        crop.resize((crop.width*6,crop.height*6),Image.Resampling.NEAREST).save(R/f'visual/original-component-{index:03}.png')
print('Original-derived enlarged finding proofs saved; no PDF source content outside assigned pages accessed.')
