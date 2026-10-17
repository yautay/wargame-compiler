"""Independently authored physical partitions after fresh original-page inspection.

All coordinates below are unrotated top-left source PDF points. Diagram tiles
partition the displayed field; overlapping component crops are explicitly context
and contribute no denominator. They document visible layers, never inferred play.
"""
import json
from pathlib import Path

ROOT = Path(__file__).parent
SPECS = []


def add(page, key, box, kind, observation, role='inventory', group=None):
    SPECS.append(dict(page=page, key=f'ig2b08:p{page}:{key}', points=box,
                      kind=kind, observation=observation, role=role, group=group))


def text(page, side, rows):
    x0, x1 = (45, 297) if side == 'L' else (315, 567)
    for key, y0, y1, kind, observation in rows:
        add(page, key, [x0, y0, x1, y1], kind, observation)


for page in (29, 30, 31, 32):
    add(page, 'running-header', [45, 22, 567, 41], 'editorial', 'Running title, edition, printed page number and horizontal rule; retained, not excluded.')
    add(page, 'copyright', [260, 748, 349, 759], 'editorial', 'Copyright footer; retained, not an authorized exclusion.')

text(29, 'L', [
    ('incoming-example', 52, 137, 'example', 'Upper-left italic paragraph continues the accepted page-28 example; begins rounded up to 4:1 and ends not rout yet.'),
    ('celt-example', 142, 239, 'example', 'Italic Celt C frontal-attack calculation paragraph.'),
    ('collapse-example', 574, 671, 'example', 'The Collapse paragraph below first diagram.'),
    ('collapse-check-example', 675, 724, 'example', 'Next-step 8.47[2] example paragraph.')])
text(29, 'R', [
    ('advance-example', 52, 113, 'example', 'Last-step 8.47[3] advance example above second diagram.'),
    ('advance-heading', 447, 460, 'heading', '8.5 Advance After Combat heading.'),
    ('advance-design-note', 462, 489, 'note', 'Blue design note immediately below 8.5.'),
    ('advance-851', 495, 616, 'clause', '8.51 paragraph; one contiguous numbered clause.'),
    ('advance-design-discussion', 619, 719, 'note', 'Blue design discussion after 8.51.')])

text(30, 'L', [
    ('advance-852', 52, 101, 'clause', '8.52 paragraph above four diagram panels.'),
    ('caption-no-advance', 291, 304, 'legend', 'No Advance caption.'),
    ('caption-advance', 503, 516, 'legend', 'Advance caption.'),
    ('advance-853', 521, 678, 'clause', '8.53 paragraph below four diagram panels.'),
    ('advance-854-start', 682, 731, 'clause', '8.54 begins lower-left and continues at top-right.')])
# Captions are side-by-side, not a single mixed line.
for key in ('caption-no-advance', 'caption-advance'):
    next(s for s in SPECS if s['key'].endswith(':'+key))['points'][2] = 166
add(30, 'caption-pivot', [175, 291, 297, 304], 'legend', 'Pivot Advance caption.')
add(30, 'caption-wheel', [175, 503, 297, 516], 'legend', 'Advance with Wheel caption.')
text(30, 'R', [
    ('advance-854-end', 52, 77, 'clause', 'Top-right continuation of 8.54.'),
    ('advance-855', 82, 119, 'clause', '8.55 paragraph.'),
    ('advance-856', 123, 148, 'clause', '8.56 paragraph.'),
    ('pursuit-heading', 155, 168, 'heading', '8.6 Cavalry Pursuit heading.'),
    ('pursuit-history', 170, 258, 'note', 'Tan historical note.'),
    ('beneventum-note', 265, 293, 'note', 'Gray play note.'),
    ('pursuit-861-intro', 299, 372, 'clause', '8.61 introduction before five bullets.'),
    ('pursuit-861-b1', 374, 399, 'clause', 'First pursuit exception bullet.'),
    ('pursuit-861-b2', 400, 425, 'clause', 'Second pursuit exception bullet.'),
    ('pursuit-861-b3', 426, 438, 'clause', 'Third pursuit exception bullet.'),
    ('pursuit-861-b4', 439, 464, 'clause', 'Fourth pursuit exception bullet.'),
    ('pursuit-861-b5', 465, 478, 'clause', 'Fifth pursuit exception bullet.'),
    ('pursuit-861-close', 481, 506, 'clause', 'Closing paragraph after exception bullets.'),
    ('pursuit-862-intro', 511, 560, 'clause', '8.62 introduction and procedure alternatives.'),
    ('pursue-intro', 564, 637, 'clause', 'Pursue bold lead-in and introductory paragraph.'),
    ('pursue-b1', 640, 665, 'clause', 'First direction bullet.'),
    ('pursue-b2', 666, 691, 'clause', 'Second direction bullet.'),
    ('pursue-next-page', 695, 732, 'clause', 'Bottom-right paragraph continues on physical page 31.')])

text(31, 'L', [
    ('pursue-continuation', 52, 114, 'clause', 'Top-left continuation from page 30.'),
    ('pursuit-range-note', 116, 156, 'note', 'Gray play note about leader range.'),
    ('pursuit-off-map', 163, 200, 'clause', 'Off-map paragraph before Break-Off.'),
    ('break-off', 204, 217, 'clause', 'Break-Off bullet.'),
    ('finished-close', 269, 294, 'clause', 'Full-width lower lines of 8.63; linked to upper wrapped text.'),
    ('zama-example', 299, 372, 'example', 'Zama example paragraph.'),
    ('routing-note', 375, 450, 'note', 'Gray play note after Zama example.'),
    ('regroup-864', 456, 553, 'clause', '8.64 Off-Map Regroup paragraph.'),
    ('off-map-865', 558, 595, 'clause', '8.65 paragraph.'),
    ('option-866', 599, 636, 'clause', '8.66 optional pursuit-rating introduction.'),
    ('rating-lcln', 640, 653, 'table', 'First pursuit rating row: LC/LN and value.'),
    ('rating-rchcbc', 658, 671, 'table', 'Second pursuit rating row: RC/HC/BC and value.'),
    ('drm-label', 675, 689, 'legend', 'DRMs label.'),
    ('drm-numidian', 690, 704, 'table', 'First modifier row.'),
    ('drm-infantry', 705, 718, 'table', 'Second modifier row.'),
    ('drm-charisma', 719, 733, 'table', 'Third modifier row.'),
    ('drm-zoc', 733, 746, 'table', 'Fourth modifier row.')])
add(31, 'finished-upper', [90, 221, 297, 269], 'clause', '8.63 upper lines wrap to the right of the Pursuit/Finished marker.')
add(31, 'finished-marker', [45, 225, 82, 262], 'diagram', 'Pursuit/Finished marker artwork; distinct from wrapped 8.63 text.')
text(31, 'R', [
    ('tables-heading', 52, 65, 'heading', '8.7 The Combat Tables heading.'),
    ('chart-871', 68, 93, 'clause', '8.71 chart description; actual chart not present here.'),
    ('chart-872', 98, 171, 'clause', '8.72 chart description.'),
    ('chart-873', 175, 212, 'clause', '8.73 chart description.'),
    ('chart-874', 217, 254, 'clause', '8.74 table description.'),
    ('chart-875', 258, 295, 'clause', '8.75 chart description.'),
    ('special-units-heading', 309, 327, 'heading', '9.0 Special Combat Units heading.'),
    ('elephant-heading', 333, 346, 'heading', '9.1 War Elephants heading.'),
    ('elephant-history', 347, 471, 'note', 'Tan historical note about war elephants.'),
    ('pass-through-lower', 528, 566, 'clause', 'Full-width lower lines of 9.11 introduction.'),
    ('pass-through-b1', 567, 580, 'clause', 'First Pass-Thru restriction bullet.'),
    ('pass-through-b2', 581, 594, 'clause', 'Second Pass-Thru restriction bullet.'),
    ('pass-through-b3', 595, 620, 'clause', 'Third Pass-Thru restriction bullet.'),
    ('pass-through-close', 623, 660, 'clause', 'Two-defender paragraph.'),
    ('pass-through-procedure', 665, 678, 'clause', 'Numbered procedure lead-in.'),
    ('pass-through-step1', 680, 705, 'clause', 'Pass-Thru step 1.'),
    ('pass-through-step2', 706, 743, 'clause', 'Pass-Thru step 2; steps continue on page 32.')])
add(31, 'elephant-counter', [315, 484, 352, 521], 'diagram', 'Africa elephant counter artwork beside 9.11.')
add(31, 'pass-through-upper', [360, 480, 567, 528], 'clause', '9.11 introductory lines wrap to the right of elephant counter.')

text(32, 'L', [
    ('pass-through-step3', 52, 101, 'clause', 'Pass-Thru step 3 continued from page 31.'),
    ('pass-through-step4', 103, 152, 'clause', 'Pass-Thru step 4.'),
    ('pass-through-design', 154, 218, 'note', 'Blue design note after numbered procedure.'),
    ('screens-912-intro', 225, 298, 'clause', '9.12 first paragraph.'),
    ('screens-912-close', 302, 363, 'clause', '9.12 second paragraph.'),
    ('tower-913', 368, 417, 'clause', '9.13 Tower Riders paragraph.'),
    ('tower-design', 419, 458, 'note', 'Blue design note about towers.'),
    ('rampage-914-intro', 465, 514, 'clause', '9.14 introduction before split table.')])
# Each table header and result cell is independently selected.
for key, box, obs in [
    ('table-die-header', [45,519,96,534], 'Die Roll header cell.'),
    ('table-result-header', [96,519,297,534], 'Result header cell.'),
    ('table-zero-key', [45,534,96,585], 'Die roll 0 key cell.'),
    ('table-zero-result', [96,534,297,585], 'Die roll 0 result cell.'),
    ('table-one-six-key', [45,585,96,648], 'Die roll 1-6 key cell.'),
    ('table-one-six-result', [96,585,297,648], 'Die roll 1-6 result cell.'),
    ('table-seven-nine-key', [315,55,366,166], 'Die roll 7-9 key cell in top-right continuation.'),
    ('table-seven-nine-result', [366,55,567,166], 'Die roll 7-9 result cell in top-right continuation.')]:
    add(32, key, box, 'table', obs, group='rampage-table')
text(32, 'R', [
    ('rampage-immediate', 180, 217, 'clause', 'Paragraph following table continuation.'),
    ('rampage-example-caption', 303, 340, 'example', 'Italic example caption below two-elephant diagram.'),
    ('rampage-movement', 344, 453, 'clause', 'Rampaging elephant movement paragraph.'),
    ('rampage-stacks', 458, 519, 'clause', 'Stack and leader paragraph.'),
    ('rampage-repeat', 523, 536, 'clause', 'Repetition lead-in before four bullets.'),
    ('rampage-stop1', 538, 551, 'clause', 'First ending-condition bullet.'),
    ('rampage-stop2', 552, 565, 'clause', 'Second ending-condition bullet.'),
    ('rampage-stop3', 565, 590, 'clause', 'Third ending-condition bullet.'),
    ('rampage-stop4', 590, 615, 'clause', 'Fourth ending-condition bullet.'),
    ('rampage-leader', 619, 692, 'clause', 'Leader paragraph.'),
    ('rampage-exit', 697, 723, 'clause', 'Last paragraph ends Each Rampage is and continues in exact page-33 context rectangle.')])
add(33, 'exit-context', [45,50,306,80], 'clause', 'Exactly two initial continuation lines completing page-32 paragraph; following note excluded from access.', 'context')


def diagram(page, key, xs, ys, components, obs):
    # Disjoint tiles expose the whole field, including otherwise easily omitted hex
    # outlines and visual backgrounds. Component crops can overlap these tiles.
    for r, (y0,y1) in enumerate(zip(ys,ys[1:]),1):
        for c, (x0,x1) in enumerate(zip(xs,xs[1:]),1):
            add(page, f'{key}-tile-{r}-{c}', [x0,y0,x1,y1], 'diagram',
                f'{obs} Physical field tile row {r}, column {c}; component mapping is in component-ledger.json.', group=key)
    for label, box, description in components:
        add(page, f'{key}-component-{label}', box, 'diagram', description,
            'context', key)


diagram(29, 'collapse-diagram', [55,115,171,244,289], [248,295,337,383,434,482,526,566], [
    ('a-label',[116,276,129,291],'Letter A locator.'),
    ('a-phalanx',[137,281,169,342],'Blue Phalanx A counter.'),
    ('a-bastarni',[95,295,126,327],'Green Bastarni counter.'),
    ('a-hits',[120,317,145,350],'Visible 2 hit-marker stack behind Phalanx A.'),
    ('b-label',[123,388,137,402],'Letter B locator.'),
    ('b-phalanx',[138,366,169,424],'Blue Phalanx B counter.'),
    ('b-hits',[119,403,146,434],'Visible 2 hit marker behind B.'),
    ('c-label',[103,496,117,508],'Letter C locator.'),
    ('c-celt',[128,483,168,528],'Green Celt C counter and visible counter edge.'),
    ('c-hits',[106,496,133,527],'Visible 4 marker behind Celt C.'),
    ('d-label',[121,531,132,542],'Letter D locator.'),
    ('d-celt',[128,526,168,561],'Green Celt D counter.'),
    ('t',[173,253,222,298],'Defender T counter and letter.'),
    ('u',[173,298,241,337],'Defender U counter, 1 marker and letter.'),
    ('v',[173,337,241,383],'Tribune/defender V stack, F and 4 markers, letter V.'),
    ('w',[245,373,289,426],'Defender W and Routed/TQ=1 marker with letter W.'),
    ('x',[173,410,242,463],'Defender X counter and 6/2 markers with letter X.'),
    ('y',[173,463,241,506],'Defender Y and 4 marker with letter Y.'),
    ('z',[173,505,241,552],'Defender Z and 5 marker with letter Z.')],
    'First combat snapshot below Celt C example; hex field and A-D/T-Z labels.')

diagram(29, 'advance-diagram', [325,400,443,497,558], [120,168,209,260,298,337,379,438], [
    ('a',[364,152,440,222],'A/Bastarni/Phalanx stack and 2 marker with A label.'),
    ('t',[444,127,491,163],'Defender T counter and label.'),
    ('u',[444,168,508,204],'Defender U counter, 1 marker and label.'),
    ('v',[444,207,511,254],'Tribune/defender V, F and 4 markers and label.'),
    ('b-origin',[404,237,439,298],'Translucent origin of Phalanx B.'),
    ('b-destination',[443,259,478,320],'Opaque Phalanx B destination counter.'),
    ('b-arrow',[421,265,452,288],'Green advance arrow for B.'),
    ('b-hits-label',[396,262,451,329],'B label and visible 2 marker; overlapping detail crop.'),
    ('w',[512,240,553,291],'W counter and Routed/TQ=1 marker and label.'),
    ('x',[511,293,554,344],'X counter and Routed/TQ=1 marker and label.'),
    ('x-arrow',[486,302,523,320],'Yellow horizontal arrow to X.'),
    ('y',[443,334,511,373],'Y counter, 4 marker and label.'),
    ('c-origin',[403,355,439,388],'Translucent Celt C origin.'),
    ('c-destination',[435,370,476,410],'Rotated Celt C destination.'),
    ('c-arrow',[418,369,451,393],'Green arrow and pivot from C origin.'),
    ('c-hits',[465,385,495,418],'3 marker behind C.'),
    ('d',[395,398,439,433],'D label and counter.'),
    ('z',[511,367,554,416],'Z counter, Routed/TQ=1 marker and label.'),
    ('z-arrow',[486,382,524,402],'Yellow horizontal arrow to Z.')],
    'Second combat snapshot beneath last-step example; moved and routed stacks.')

# Four separately captioned panels. Each unit/arrow receives a detail crop.
panels = [
    ('no-advance',45,101,171,288, [
        ('routed',[56,116,99,165],'Routed marker and blue defender counter.'),
        ('middle',[121,163,160,208],'Middle blue defender counter.'),
        ('left',[51,206,94,249],'Lower-left blue defender counter.'),
        ('phalanx',[89,209,158,269],'Red Phalanx counter; no motion arrow.')]),
    ('pivot-advance',173,101,297,288,[
        ('routed',[179,116,222,165],'Routed marker and blue defender counter.'),
        ('left',[176,206,219,249],'Left blue defender counter.'),
        ('origin',[233,201,282,258],'Translucent red origin counter.'),
        ('destination',[219,197,250,254],'Vertical red destination counter.'),
        ('arrow',[214,151,234,194],'Cyan curved arrow.')]),
    ('advance',45,313,171,499,[
        ('routed',[63,318,97,348],'Routed marker.'),
        ('upper-right',[92,313,131,357],'Upper-right blue counter.'),
        ('upper-left',[53,334,93,377],'Upper-left blue counter.'),
        ('middle',[53,373,95,416],'Middle blue counter.'),
        ('lower',[53,414,95,458],'Lower blue counter.'),
        ('phalanx',[90,382,155,447],'Opaque red destination and translucent origin edges.'),
        ('arrows',[104,345,141,476],'Cyan curved and black forward arrows; overlapping visual detail.')]),
    ('advance-wheel',173,313,297,499,[
        ('routed',[192,318,226,349],'Routed marker.'),
        ('upper-right',[218,313,260,357],'Upper-right blue counter.'),
        ('upper-left',[181,334,222,378],'Upper-left blue counter.'),
        ('middle',[181,373,224,418],'Middle blue counter.'),
        ('lower',[181,414,224,459],'Lower blue counter.'),
        ('destination',[220,378,252,434],'Opaque vertical red Phalanx destination.'),
        ('origins',[224,383,283,474],'Translucent diagonal red origins behind destination.'),
        ('arrows',[202,343,268,440],'Cyan and black turning arrows; overlapping visual detail.')])]
for key,x0,y0,x1,y1,components in panels:
    diagram(30,key,[x0,(x0+x1)//2,x1],[y0,(y0+y1)//2,y1],components,
            f'{key} panel: hex field, unit counters, status markers, paths and visible origin/destination layers.')

diagram(32, 'rampage-compass', [350,445,533], [219,298], [
    ('before',[360,228,414,290],'Upright Africa elephant counter within hex.'),
    ('after',[465,228,521,290],'Rotated elephant counter within second hex.'),
    ('six',[468,219,480,233],'Compass label 6.'),
    ('one',[505,219,518,233],'Compass label 1.'),
    ('two',[523,251,533,265],'Compass label 2.'),
    ('three',[504,284,518,298],'Compass label 3.'),
    ('four',[469,284,482,298],'Compass label 4.'),
    ('five',[450,251,462,265],'Compass label 5.')],
    'Two-elephant example diagram, hex outlines and six compass labels.')

# The two compact rating rows have no drawn grid, but both cells are explicit.
for row,cut in [('rating-lcln',80),('rating-rchcbc',98.5)]:
    s=next(s for s in SPECS if s['key']==f'ig2b08:p31:{row}')
    x0,y0,x1,y1=s['points']
    s['points']=[x0,y0,cut,y1]
    s['observation']+=' Unit-type key cell.'
    add(31,row+'-value',[cut,y0,108,y1],'table','Numeric value cell for '+row+'.',group='pursuit-ratings')

# Additional stack-layer selections: the full field tiles remain disjoint while
# each visible counter/status overlay/letter is available as a bounded detail.
for key,box,obs in [
    ('u-counter',[174,299,205,330],'U defender counter.'),
    ('u-hit',[196,303,224,333],'U 1 hit marker.'),
    ('u-letter',[225,306,239,319],'U letter.'),
    ('v-counter',[174,339,205,370],'V defender stack and Tribune artwork.'),
    ('v-hit',[196,350,224,380],'V 4 hit marker.'),
    ('v-letter',[225,349,239,362],'V letter.'),
    ('x-counter',[174,423,205,455],'X defender counter.'),
    ('x-hits',[195,411,223,460],'X 6 and 2 hit-marker layers.'),
    ('x-letter',[225,432,239,446],'X letter.'),
    ('y-counter',[174,466,205,497],'Y defender counter.'),
    ('y-hit',[196,478,224,506],'Y 4 hit marker.'),
    ('y-letter',[225,474,239,488],'Y letter.'),
    ('z-counter',[174,509,205,540],'Z defender counter.'),
    ('z-hit',[196,509,224,550],'Z 5 hit marker and underlying visible layer.'),
    ('z-letter',[225,517,239,532],'Z letter.')]:
    add(29,'collapse-diagram-component-'+key,box,'diagram',obs,'context','collapse-diagram')

if __name__ == '__main__':
    (ROOT/'author-selections.json').write_text(json.dumps(SPECS,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'authored_selections':len(SPECS),'inventory':sum(s['role']=='inventory' for s in SPECS),'context_details':sum(s['role']=='context' for s in SPECS)}))
