"""Task-owned explicit source partition; no gameplay interpretation."""
import copy
import datetime
import json
from pathlib import Path

import pdfplumber
from wgc.sources.inventory import assign, file_pin

ROOT = Path.cwd()
OUT = Path(__file__).parent
SESSION = ROOT / 'private/workflow/orchestrator/20261015T200250Z-56a048a1/002-IG-2B04-executor-ad82c8e3'
TASK = json.loads((SESSION / 'task.json').read_text())
CONTRACT = json.loads((ROOT / TASK['inventory_contract']['path']).read_text())
COMMON = {k: json.loads((OUT / 'claim.json').read_text())[k] for k in
          ('role', 'actor', 'task', 'model', 'reasoning', 'configuration_evidence', 'configuration_sha256')}


def save(name, value):
    path = OUT / name
    assert not path.exists(), path
    path.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')


# Explicit visual reading order, with pixel boundaries on 1224 x 1584 original renders.
# Consecutive rows tile each column. Safe whitespace snapping uses assigned glyph
# geometry only and never chooses/classifies source units.
ROWS = {
    13: {
        'left': [
            (184, 'exception-elite-momentum', 'clause', 'Opening Exception referring to Elite activation (5.5); complete visible paragraph, preceding anchor outside scope.'),
            (222, 'heading-5.4', 'heading', '5.4 THE TRUMP OPTION'),
            (425, 'design-note-trump', 'note', 'Blue DESIGN NOTE; entire paragraph and highlighted background.'),
            (607, '5.41', 'clause', '5.41 Active Player Trump Option; complete paragraph.'),
            (713, 'example-5.41', 'example', 'Cannae example associated with 5.41.'),
            (772, '5.42-intro', 'clause', '5.42 Inactive Player Trump Options introductory paragraph.'),
            (974, '5.42-option-1', 'clause', 'Numbered 1. Trumping the Trump paragraph.'),
            (1105, 'example-5.42-option-1', 'example', 'Example following numbered option 1.'),
            (1189, '5.42-option-2', 'clause', 'Numbered 2. Momentum Trump paragraph.'),
            (1343, 'example-5.42-option-2', 'example', 'Example following numbered option 2.'),
            (1425, '5.42-return', 'clause', 'Return to standard lowest-rated-leader procedure paragraph.'),
            (1488, '5.43', 'clause', '5.43 complete visible paragraph.')],
        'right': [
            (204, '5.44-opening-row', 'split', 'Opening 5.44 text beside marker.'),
            (330, '5.44-continuation', 'clause', '5.44 text below marker; continues same paragraph.'),
            (539, 'play-note-no-momentum', 'note', 'Gray PLAY NOTE associated with Trump/No Momentum.'),
            (621, '5.45', 'clause', '5.45 complete visible paragraph.'),
            (708, '5.46', 'clause', '5.46 complete visible paragraph.'),
            (746, 'heading-5.5', 'heading', '5.5 ELITE COMMANDER INITIATIVE'),
            (827, 'design-note-elite', 'note', 'Blue DESIGN NOTE below 5.5 heading.'),
            (1060, '5.51', 'clause', '5.51 paragraph including inline red triangle symbol and EIO definition.'),
            (1189, '5.52', 'clause', '5.52 complete paragraph.'),
            (1319, '5.53', 'clause', '5.53 complete paragraph.'),
            (1488, 'example-5.53-start', 'example', 'Zama example starts here and ends mid-sentence at definite; continues on physical page14.')]
    },
    14: {
        'left': [
            (181, 'example-5.53-end', 'example', 'Opening italic paragraph completes the page13 Zama example.'),
            (248, 'heading-6.0', 'heading', '6.0 MOVEMENT'),
            (284, 'heading-6.1', 'heading', '6.1 MOVEMENT ALLOWANCES'),
            (392, 'design-note-movement', 'note', 'Blue DESIGN NOTE about movement allowances.'),
            (501, '6.11', 'clause', '6.11 complete paragraph.'),
            (582, '6.12', 'clause', '6.12 complete paragraph.'),
            (690, 'example-6.12', 'example', 'Hastati/Tribune example.'),
            (820, '6.13', 'clause', '6.13 complete paragraph with references.'),
            (868, 'exception-6.13', 'clause', 'Exception for Skirmisher units.'),
            (955, 'play-note-moved-row', 'split', 'Gray PLAY NOTE and separate Moved marker.'),
            (1136, '6.14', 'clause', '6.14 Leaders paragraph, including parenthetical leader elephants.'),
            (1245, '6.15', 'clause', '6.15 complete paragraph.'),
            (1488, 'blank-left-lower', 'editorial', 'Blank area below column text; inventoried without an exclusion claim.')],
        'right': [
            (133, 'heading-6.2', 'heading', '6.2 TERRAIN'),
            (292, 'historical-note-terrain', 'note', 'Tan HISTORICAL NOTE below Terrain heading.'),
            (404, '6.21', 'clause', '6.21 complete paragraph.'),
            (485, 'example-6.21', 'example', 'Cynoscephalae movement-cost example.'),
            (736, '6.22', 'clause', '6.22 complete paragraph.'),
            (819, 'example-6.22', 'example', 'HU/MI cohesion-hit example.'),
            (956, 'play-note-terrain', 'note', 'Gray PLAY NOTE about rough and hilly terrain.'),
            (1039, '6.23', 'clause', '6.23 complete paragraph.'),
            (1216, '6.24', 'clause', '6.24 complete paragraph including named terrain examples.'),
            (1308, 'historical-note-cannae', 'note', 'Tan HISTORICAL NOTE about Cannae.'),
            (1371, '6.25', 'clause', '6.25 complete paragraph.'),
            (1488, '6.26', 'clause', '6.26 complete paragraph; reference 8.74 remains unresolved in this scope.')]
    },
    15: {
        'left': [
            (184, '6.27', 'clause', '6.27 The Movement Cost Chart paragraph; chart itself is not on this page.'),
            (222, 'heading-6.3', 'heading', '6.3 MOVEMENT PROCEDURES'),
            (373, '6.31', 'clause', '6.31 complete paragraph.'),
            (480, '6.32-opening', 'clause', '6.32 opening paragraph.'),
            (539, '6.32-phalanx', 'clause', 'Separate Phalanx paragraph completing 6.32.'),
            (578, 'heading-6.4', 'heading', '6.4 PHALANX UNITS'),
            (690, 'historical-note-phalanx', 'note', 'Tan HISTORICAL NOTE about the word Phalanx.'),
            (854, 'design-note-phalanx', 'note', 'Blue DESIGN NOTE about phalanx movement.'),
            (1128, '6.41', 'clause', '6.41 complete paragraph; includes printed superscript th in 5th.'),
            (1308, '6.42', 'clause', '6.42 complete paragraph.'),
            (1488, '6.43', 'clause', '6.43 The Front-to-Flank Maneuver paragraph; complete at column bottom.')],
        'right': [
            (289, 'diagram-front-to-flank', 'diagram', 'Hex grid, opaque red Macedonian Phalanx counter, faded prior counter, pivot arrow; all included.'),
            (342, 'caption-front-to-flank', 'legend', 'Italic Macedonian Phalanx caption below diagram.'),
            (572, '6.44', 'clause', '6.44 The Wheeling Maneuver paragraph.'),
            (774, 'example-6.44', 'example', 'Cannae example below 6.44; complete paragraph.'),
            (910, '6.45', 'clause', '6.45 The Reverse Face Maneuver paragraph.'),
            (949, 'heading-6.5', 'heading', '6.5 ORDERLY WITHDRAWAL'),
            (1122, '6.5-intro', 'clause', 'Unnumbered Orderly Withdrawal introductory paragraph.'),
            (1235, 'play-note-withdrawal', 'note', 'Gray PLAY NOTE about the extended example.'),
            (1488, '6.51-start', 'clause', '6.51 starts here and continues after away on physical page16.')]
    },
    16: {
        'left': [
            (279, '6.51-continuation', 'clause', 'Opening paragraph continues physical page15 6.51, starting from the moving unit.'),
            (310, '6.51-exceptions-heading', 'heading', 'Exceptions: italic bold label.'),
            (384, '6.51-exception-1', 'clause', 'First bulleted exception, Skirmisher units.'),
            (464, '6.51-exception-2', 'clause', 'Second bulleted exception, routed/raised-MA units.'),
            (548, '6.51-missile', 'clause', 'Missile-fire timing paragraph following exceptions.'),
            (685, 'play-note-two-hexes', 'note', 'Gray PLAY NOTE about any eligible friendly unit within two hexes.'),
            (793, 'example-6.51-1', 'example', 'EXAMPLE #1 Velites and Hastati.'),
            (881, 'example-6.51-2', 'example', 'EXAMPLE #2 cavalry and Elephant.'),
            (1286, 'diagram-withdrawal', 'diagram', 'Entire hex grid, shaded hexes, Front/Flank/Rear labels, blue Skirmisher and red Principes counters.'),
            (1394, 'example-6.51-3', 'example', 'EXAMPLE #3 caption below diagram; complete italic paragraph.'),
            (1488, 'blank-left-lower', 'editorial', 'Blank area below example3.')],
        'right': [
            (250, '6.52-intro', 'clause', '6.52 introductory paragraph ending with additional penalty situations.'),
            (328, '6.52-penalty-1', 'clause', 'Numbered penalty 1, Roman LG units.'),
            (404, '6.52-penalty-2', 'clause', 'Numbered penalty 2, other withdrawing infantry.'),
            (553, '6.52-penalty-3', 'clause', 'Numbered penalty 3 and reference to diagram above Example3.'),
            (770, 'historical-note-withdrawal', 'note', 'Tan HISTORICAL NOTE about withdrawal and training.'),
            (830, '6.53', 'clause', '6.53 complete paragraph.'),
            (960, '6.54', 'clause', '6.54 complete paragraph.'),
            (1066, '6.55-opening', 'clause', '6.55 first paragraph; stacking reference 6.6.'),
            (1173, '6.55-mounted-archers', 'clause', 'Mounted Archers paragraph completing visible 6.55 body.'),
            (1311, 'play-note-6.55', 'note', 'Gray PLAY NOTE completes the visible page at 2 or more.'),
            (1488, 'blank-right-lower', 'editorial', 'Blank area below final play note.')]
    }
}


def main():
    records, observations = [], []
    pdfpath = ROOT / CONTRACT['inputs']['pdf']['path']
    with pdfplumber.open(pdfpath) as pdf:
        for number, columns in ROWS.items():
            page = pdf.pages[number - 1]
            chars = page.chars
            def snap(y, x0, x1):
                if y in (90, 1488):
                    return y
                candidates = sorted(range(y - 12, y + 13), key=lambda q: (abs(q-y), q))
                for q in candidates:
                    if not any(c['x0']*2 < x1 and c['x1']*2 > x0 and c['top']*2-1 < q < c['bottom']*2+1 for c in chars):
                        return q
                raise ValueError(('No safe boundary', number, y))

            def add(key, kind, box, observation):
                norm = [box[0]*1000000//1224, box[1]*1000000//1584,
                        box[2]*1000000//1224, box[3]*1000000//1584]
                records.append({'key':f'b04:p{number}:{key}', 'pdf_page':number,
                                'kind':kind, 'box':norm, 'render_box_pixels':box,
                                'observation':observation})

            add('running-header', 'editorial', [0,0,1224,90], 'Running title, horizontal rule and printed page label; no exclusion authorization inferred.')
            add('outer-left', 'editorial', [0,90,80,1488], 'Blank outer margin.')
            for column, x0, x1 in [('left',80,604), ('right',620,1144)]:
                y0 = 90
                for y, key, kind, observation in columns[column]:
                    y1 = snap(y,x0,x1)
                    if key == '5.44-opening-row':
                        add('marker-no-momentum', 'diagram', [x0,y0,714,y1], 'Complete TRUMPED/NO Momentum marker and surrounding blank area.')
                        add('5.44-opening', 'clause', [714,y0,x1,y1], observation)
                    elif key == 'play-note-moved-row':
                        add('play-note-moved', 'note', [x0,y0,490,y1], 'PLAY NOTE text and gray background; marker separately inventoried.')
                        add('marker-moved', 'diagram', [490,y0,576,y1], 'Complete Moved marker, black label and orange checker pattern.')
                        add('play-note-moved-edge', 'editorial', [576,y0,x1,y1], 'Right edge of note background.')
                    else:
                        add(key, kind, [x0,y0,x1,y1], observation)
                    y0 = y1
            add('column-gutter', 'editorial', [604,90,620,1488], 'Blank inter-column gutter.')
            add('outer-right', 'editorial', [1144,90,1224,1488], 'Blank outer margin.')
            add('footer', 'editorial', [0,1488,1224,1584], 'Copyright footer and bottom margin; preserved as editorial inventory, no exclusion claim.')
            observations.append({'physical_page':number, 'original_png':file_pin(ROOT,(OUT/f'original-pages/page-{number}.png').relative_to(ROOT).as_posix()),
                'observation':{13:'Inspected both columns, opening exception, 5.4/5.5 headings, two marker/symbol forms, design/play notes, all examples and incomplete final example.',
                               14:'Inspected opening continuation, 6.0/6.1/6.2 headings, Moved marker, all clauses/examples, two historical notes and lower blank area.',
                               15:'Inspected 6.27, 6.3/6.4/6.5 headings, all clauses/notes/examples, complete pivot diagram and caption, incomplete final 6.51 paragraph.',
                               16:'Inspected opening 6.51 continuation, both bullets, three examples, complete annotated withdrawal diagram, three numbered 6.52 penalties, all final clauses and notes.'}[number]})
    # Persist explicit new bindings once; all complete regenerations begin from this
    # same registry, retaining every accepted and retired entry.
    registry = json.loads((ROOT / CONTRACT['inputs']['identity_registry']['path']).read_text())
    for rec in records:
        rec['id'] = assign(registry,'region',rec['key'])
    save('authored-registry.json', registry)
    save('authored-regions.json', {**COMMON,'format':'wgc-authored-inventory-spec-1','source':CONTRACT['inputs']['pdf'],
         'coordinate_frame':'unrotated-effective-crop-top-left-page-millionths','original_render_pixels':[1224,1584],
         'method':'Explicit units and reading order authored from fresh original-page visual inspection; row boundaries snapped only to nearby glyph-free whitespace.',
         'regions':records})
    save('original-inspection.json',{**COMMON,'format':'wgc-original-inspection-1',
         'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'dpi':144,'source':CONTRACT['inputs']['pdf'],
         'provenance':CONTRACT['inputs']['provenance'],'pages':observations,
         'entry_boundary':{'observation':CONTRACT['boundary'],'assigned_page13':'Opens with an Exception referencing 5.5; association with the inaccessible preceding sentence remains unresolved.'},
         'exit_boundary':{'physical_page':16,'observation':'Final play note is visibly complete; chapter continuation and any page17 relationship remain unresolved. No adjacent page read.'},
         'semantic_acceptance_granted':False})
    print(json.dumps({'authored_regions':len(records),'assigned_pages':[13,14,15,16]}))


if __name__ == '__main__':
    main()
