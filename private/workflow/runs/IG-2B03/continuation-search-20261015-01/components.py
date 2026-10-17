"""Independent source-pinned counter component locators; zero denominator."""
import copy
from pathlib import Path
from build import ROOT, OUT, COMMON, load, write
from wgc.sources.inventory import assign, make_region, seal, validate, file_pin
from wgc.sources.pdf import extract_evidence

# Bounds are visually selected in the fresh 600-DPI original counter details.
# Each uses page millionths derived outward from a 310 x 310 detail frame.
SPECS = {
 9: [
 ('field-and-border',[0,0,310,310],'White field within dark rectangular outline.'),
 ('name',[100,32,275,85],'Visible name T.Varro; punctuation and glyph spacing retained in the image.'),
 ('star-strip',[34,34,92,210],'Dark strip containing three gold stars.'),
 ('star-top',[37,39,88,94],'Upper gold star.'),
 ('star-middle',[37,96,88,151],'Middle gold star.'),
 ('star-bottom',[37,153,88,207],'Lower gold star.'),
 ('central-art',[101,85,218,214],'Gold helmet/profile, red crest and purple background. Image observation only.'),
 ('red-disc-1',[220,102,282,173],'Red circular field containing yellow 1.'),
 ('bottom-left-4',[31,215,85,281],'Black 4 on white field.'),
 ('bottom-second-4',[103,211,151,281],'Second black 4 on white field.'),
 ('bottom-boxed-1',[151,209,217,284],'White 1 in gray rectangular field.'),
 ('bottom-boxed-0',[221,207,280,285],'Yellow 0 in black rectangular field.')],
 11: [
 ('field-and-border',[0,0,310,310],'Pale green field within dark rectangular outline.'),
 ('name',[95,32,279,85],'Visible name Elephant 1; visual glyph observation only.'),
 ('star-strip',[34,33,92,207],'Two gold stars on dark strip; lower part of strip is blank.'),
 ('star-top',[37,37,88,92],'Upper gold star.'),
 ('star-bottom',[37,94,88,150],'Lower gold star.'),
 ('central-art',[98,84,212,211],'Gold/yellow silhouette with brown vertical detail and dark features on purple field; precise artwork identity remains uncertain.'),
 ('bottom-left-4',[31,212,84,281],'Black 4 on pale green field.'),
 ('bottom-second-1',[105,207,148,283],'Black 1 on pale green field.'),
 ('bottom-boxed-dash',[151,207,216,284],'White horizontal dash in gray rectangular field; not interpreted as a numeric value.'),
 ('bottom-boxed-0',[220,207,279,284],'Yellow 0 in black rectangular field.')]
}

def run():
    doc=load(OUT/'authored/inventory.json')
    observations=[]
    for n,specs in SPECS.items():
        parent=next(r for r in doc['regions'] if r['key']==('spqr5e:p09:44-commander-counter' if n==9 else 'spqr5e:p11:49-elephant-counter'))
        page=next(p for p in doc['pages'] if p['id']==parent['page_id'])
        for slug,b,observation in specs:
            pb=parent['box'];w=pb[2]-pb[0];h=pb[3]-pb[1]
            box=[pb[0]+w*b[0]//310,pb[1]+h*b[1]//310,pb[0]+(w*b[2]+309)//310,pb[1]+(h*b[3]+309)//310]
            key=parent['key']+':component:'+slug
            region=make_region(doc['registry'],key,page,box,kind='diagram',role='context',reason='Counter component observation only; parent owns inventory denominator; no verified transcription or semantics.')
            doc['regions'].append(region);doc['reading_order'].append(region['id'])
            observations.append({'page':n,'parent_region_id':parent['id'],'region_id':region['id'],'key':key,'box':box,'selection_frame_pixels':[310,310],'selection_bounds':b,'observation':observation,'denominator_units':0})
    doc=seal(doc)
    directory=OUT/'components';directory.mkdir(exist_ok=False)
    write(directory/'authored-inventory.json',doc);write(directory/'identity-registry.json',doc['registry'])
    for i,c in enumerate(observations):
        ev=extract_evidence(doc,c['region_id'],ROOT,(directory/f'component-{i+1:02d}').as_posix(),dpi=600)
        doc['evidence'].append(ev);doc=seal(doc);c['evidence_id']=ev['id']
        print('component',i+1,'/',len(observations),flush=True)
    report=validate(doc,ROOT)
    write(directory/'inventory.json',doc)
    write(directory/'validation.json',{**COMMON,'operation':'wgc.sources.inventory.validate(document, repository_root)','exit_code':0,'inventory':file_pin(ROOT,(directory/'inventory.json').as_posix()),'result':report})
    write(OUT/'component-ledger.json',{**COMMON,'components':observations,'scope':'All locators are on assigned physical pages 9 and 11. Overlap is intentional for component observations; each is context with zero denominator. Full inventory denominator remains in final-verified/inventory.json.','semantic_acceptance_granted':False})

if __name__=='__main__':run()
