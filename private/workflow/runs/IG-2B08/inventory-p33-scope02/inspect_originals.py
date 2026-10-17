"""Fresh source access restricted to assigned pages and exact context rectangle."""
import hashlib
import json
import subprocess
from pathlib import Path

import pdfplumber
from PIL import Image
from pypdf import PdfReader, PdfWriter
from pypdf.generic import RectangleObject

ROOT = Path(__file__).parent
PDF = Path('private/ig/sources/spqr-5e-official/revision-20261013T155212Z/rulebook.pdf')
assert hashlib.sha256(PDF.read_bytes()).hexdigest() == 'e5b65958ca04261058147966b10e1ab2785061fc50060390f8a4ce0e34c6d69e'
out = ROOT / 'originals'
out.mkdir(exist_ok=False)
records = []
with pdfplumber.open(PDF) as pdf:
    for number in [29, 30, 31, 32, 33]:
        prefix = out / f'page-{number}'
        args = ['pdftoppm', '-f', str(number), '-l', str(number), '-singlefile', '-r', '144', '-png']
        page = pdf.pages[number - 1]
        if number == 33:
            # Crop the ORIGINAL page before releasing any characters or text.
            page = page.crop((45, 50, 306, 80), strict=True)
            args += ['-x', '90', '-y', '100', '-W', '522', '-H', '60']
        text = page.extract_text(x_tolerance=3, y_tolerance=3, layout=False) or ''
        prefix.with_suffix('.txt').write_text(text, encoding='utf-8', newline='\n')
        words = page.extract_words(x_tolerance=3, y_tolerance=3)
        prefix.with_suffix('.words.json').write_text(json.dumps(words, indent=2), encoding='utf-8')
        subprocess.run(args + [str(PDF), str(prefix)], check=True, capture_output=True)
        if number == 33:
            writer = PdfWriter()
            crop = writer.add_page(PdfReader(PDF, strict=True).pages[32])
            crop.mediabox = RectangleObject([45, 712, 306, 742])
            crop.cropbox = RectangleObject([45, 712, 306, 742])
            with prefix.with_suffix('.pdf').open('xb') as stream:
                writer.write(stream)
        with Image.open(prefix.with_suffix('.png')) as im:
            dimensions = list(im.size)
        records.append({'physical_page': number, 'box_points': [45, 50, 306, 80] if number == 33 else [0, 0, 612, 792], 'dimensions': dimensions, 'word_count': len(words), 'text_codepoints': len(text)})
(ROOT / 'original-access.json').write_text(json.dumps(records, indent=2) + '\n', encoding='utf-8')
print(json.dumps(records))
