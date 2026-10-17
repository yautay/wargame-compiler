"""Explicit reviewer readings after viewing all originals, 13 paired sheets,
four overlays, all 17 enlarged diagrams and three original-derived finding proofs.
No inferred per-image viewing timestamps are manufactured.
"""
from review_driver import *
ledger=load(D/'region-ledger-final.json')['regions'];visual=load(R/'visual-index.json')
observed='''
001|Running italic/bold title and edition suffix fully inside the frame.
002|Printed 5 alone; top-right placement matches physical page 5.
003|Whole horizontal separator line, including both ends; no body text included.
004|Two-line Triarii tail begins heavy infantry and ends as a unit class.
005|Alae Sociorum inline bold heading; first four lines end Sam- beside the counter.
006|Yellow counter, soldier/shield, ASXIVa-like identifier, CO, red-circle J, 3 LG, bottom 5 and 5. Submitted component 6 is wrong.
007|Alae paragraph resumes nites and continues through the cavalry sentence; no next Maniple heading included.
008|Maniple inline heading and full paragraph end battlefield.; no counter belongs to this paragraph.
009|Heavy Infantry heading and four opening lines end There were beside its illustration.
010|Red Aetolia counter with 4, HO, 5 HI, bottom 5/4 and hoplite; corrected component list matches source.
011|Two-line Heavy Infantry continuation ends restricted their mobility.; separate from Phalanx.
012|Phalanx heading and narrow opening prose end By the era beside wide counter.
013|Wide red Macedon 6 PH counter: soldier/spear, 10, 7 and right-side 4/5 visible; all grouped in one region.
014|Phalanx paragraph resumes of Roman ascendancy; full remaining prose ends trained tactically.
015|Legion Infantry heading and four lines end although often beside its counter.
016|Orange-framed I c / PR counter with J, 3 LG, bottom 8/5 and legionary/shield; all visible components accounted.
017|Legion continuation begins similarly armed and protected; ends spear-armed heavy infantry.
018|Medium Infantry heading and four opening lines end superior in beside counter.
019|Green Celts 12 counter with 5 MI and bottom 5/5; soldier illustration includes dark shape beside its arm. No separate J glyph observed.
020|One-line Medium Infantry completion ends light infantry.; frame does not include next heading.
021|Barbarian Infantry heading and four opening lines end typically good.
022|Green Gauls counter with identifier 5, 5 BI, bottom 7/5 and armed soldier; complete grouped illustration.
023|Barbarian continuation starts for one charge only.; ends superior organization.
024|Light Infantry heading and opening four lines end tactics and training.
025|Red Thrace counter contains small white 1 beneath name, J in black circle, 5 LI, bottom 5/5 and soldier. Submitted component list omits 1.
026|One-line Light Infantry completion: made them different from skirmishers.
027|Skirmishers full paragraph spans both wrapped words and final of maneuvering.; no standalone counter beside this entry.
028|Javelinists heading and four opening lines end which is beside repeated Thrace counter.
029|Repeated Thrace counter again has small white 1, J, 5 LI, bottom 5/5 and soldier; submitted list again omits 1.
030|Javelinists continuation starts why there are no javelinist skirmishers; ends prior to closing for combat.
031|Archers heading and four opening lines end maximum range sentence (mounted and moving).
032|Red Crete counter has identifier 2, circle A, 1 SK, bottom 4/6 and archer; later correction matches source.
033|Archers remainder starts The arrows of the day; ends Used as skirmishers.
034|Slingers heading and four opening lines end requir- beside illustration.
035|Blue Bal'ric-like name, 6, red-circle S, 1 SK, bottom 3/6 and slinger. Small name typography remains uncertain.
036|Slingers remainder resumes ing a fair amount; ends most of these troops.
037|Light Cavalry heading and four opening lines; literal final hyphenated word visually magnifi- (fi may be a ligature in extraction).
038|Green Nmdia counter with 1, J, 4 LC, bottom 8/9 and mounted soldier; no omitted number observed.
039|Centered copyright symbol and 2026 GMT Games, LLC; no body text.
040|Running italic/bold title and edition suffix fully inside frame on physical page 6.
041|Printed 6 alone at top left, separate from header line.
042|Whole separator line on page 6; no body text included.
043|Light Cavalry tail starts cent Numidian light cavalry and ends any other weapon.; joins preceding page's hyphenated fragment.
044|Lancers heading and complete three-line paragraph; no below-counter prose fragment is missing.
045|Green Celts lancer counter with 5, 4 LN and bottom 7/8, mounted spear-bearing figure; all listed components observed.
046|Heavy Cavalry heading and four lines end nowhere beside its counter.
047|Blue Crthge counter with small 3/abbreviation, 5 HC, bottom 7/8 and mounted soldier. Exact tiny abbreviation remains uncertain, as documented.
048|One-line Heavy Cavalry completion near as effective.; separate from Roman Cavalry.
049|Roman Cavalry heading and four lines end neither trained in beside its counter.
050|Beige counter shows I at upper right, 3 RC, bottom 6/8 and mounted figure with spear; corrected I observation supported.
051|Roman Cavalry continuation begins nor especially adept at; ends one would expect.
052|Elephants heading and four opening lines end a trained beside the counter.
053|Gray Africa counter with 15-like small identifier, red J and adjacent triangular a-like glyph, 5 EL, bottom 5/7, elephant/tower. Small compound glyph uncertainty remains.
054|Long Elephants remainder begins elephant corps and ends strange sounds.; no Scorpio heading included.
055|Scorpio heading and four lines end and it beside artillery counter.
056|Beige Scorpio counter with upper small 1, LI, distinct red/yellow 1 and bottom 2/3; corrected two-1 component accounting supported.
057|Scorpio final two lines end open to much debate).; lower column complete.
058|2.5 GAME SCALE heading alone, whole glyph extents retained.
059|Two complete lines describe hex distance and game-turn time; ends real time.
060|Full Size paragraph includes infantry/cavalry examples, skirmisher exception and final rating statement.
061|Full frontage paragraph includes two-hex phalanx and one-hex cavalry examples; ends one hex.
062|2.6 GAME LENGTH heading alone.
063|Two-line battle duration paragraph ends turns have passed.
064|Three-line Game Turn Track paragraph ends some of the battles.
065|Whole beige historical-note panel, italic HISTORICAL NOTE label and prose through great deal longer.; colored background inside frame.
066|2.7 LATIN heading alone.
067|Whole Latin terminology paragraph, including italic Com- / mentaries and quoted bluu.; no sequence heading included.
068|Blue 3.0 SEQUENCE OF PLAY heading fully framed.
069|Full sequence introduction ends army withdraws.; no activation heading included.
070|A. Leader Activation Phase heading alone.
071|Whole activation paragraph includes references (4.33) and (5.41), ends at this time (5.41).
072|Page-6 copyright line complete, separate from body.
073|Page-7 running title and edition complete.
074|Printed 7 at upper right; same physical-page evidence.
075|Page-7 separator line complete.
076|B. Orders Phase heading complete.
077|1. Movement and Missile Fire Segment heading complete.
078|Item a includes label and both lines; final italic or retained with item a.
079|Item b and both lines complete, ending (5.23).
080|Opponent paragraph includes Orderly Withdrawal, Manipular Line Extension and Reaction Fire; final throughout this segment. retained.
081|2. Shock Combat Segment heading complete.
082|Two-line shock introduction ends following sequence:.
083|Item a includes Shock Designation and all three lines through each individual combat.
084|Item b The Charge and parenthetical Pre-Shock TQ Check complete.
085|Item c Resolution of Possible Leader Casualties complete.
086|Item d Clash of Spears and Swords includes wrapped Shock column). line.
087|Item e Resolve the Shock complete.
088|Item f Collapse, Rout, and Cavalry Pursuit complete.
089|C. Momentum Phase or Return to A heading complete.
090|Whole Momentum paragraph including italic or and final Momentum Trump reference (5.42).
091|D. Rout and Reload Phase heading complete.
092|Numbered item 1 includes bold Rout Movement and wrapped (10.23).
093|Numbered item 2 includes bold Reload Segment and wrapped (8.18).
094|Numbered item 3 includes complete Flip and Remove instructions across three lines, including PURSUIT/FINISHED and TRUMPED.
095|E. Withdrawal Phase heading complete.
096|Full withdrawal paragraph through one side's army withdraws.; left column complete.
097|Blue 4.0 LEADERS heading complete.
098|Whole introductory leader/counter-side paragraph ends Finished side.
099|Caption, P.Scipio portrait counter, yellow-star stripe, red triangle, 8/6/2/boxed3/red-circle7; all seven labels and connecting lines inside single frame.
100|4.1 LEADER COUNTERS heading complete.
101|One-line ratings introduction ends ratings:.
102|Command Range inline heading and full paragraph, ending abilities.
103|Elite Commander inline heading and both lines, including visible red triangle in parentheses and reference 5.5.
104|Initiative inline heading and full paragraph through better the leader.
105|Line Command inline heading and four lines through number of Line Commands.
106|Strategy inline heading and both lines complete.
107|Charisma inline heading and four lines, ending stacked.
108|Blue DESIGN NOTE includes italic label and full text through control) more.; no Movement Allowance text inside frame.
109|Movement Allowance paragraph includes MP, MA 9 and Hannibal/leader-elephant parenthesis; ends actual elephant.
110|Command Restriction paragraph complete through enable Shock).; no bottom continuation required.
111|Page-7 copyright complete.
112|Page-8 running title and edition complete.
113|Printed 8 at upper left; same physical-page evidence.
114|Page-8 separator line complete.
115|Two-line 4.2 heading includes final ORDERS; no 4.21 text inside frame.
116|4.21 paragraph includes rule number and all lines through A path is obstructed by:.
117|First black bullet and enemy-unit line complete.
118|Second black bullet and enemy Zone of Control (ZOC) line complete.
119|Third black bullet and terrain line complete, including period.
120|Full following range-calculation paragraph ends instant the order is given.
121|4.22 full paragraph includes Finished side final sentence.
122|4.23 full leader-movement paragraph ends same hex.
123|4.24 full paragraph through See also 5.26.; no clipped leader/OC condition text.
124|4.25 both lines complete through ordered by his OC to do so.
125|4.3 LEADER CAPABILITIES: LINE COMMANDS heading complete on one line.
126|4.31 full paragraph includes italic instead, do not phrases and ends organizational disaster.
127|4.32 left-column paragraph complete through Eligibility Chart.; structural continuation remains right column.
128|4.32 right-column continuation begins A Line can be of any length; ends included in the Line.
129|Italic EXAMPLE paragraph fully includes Cannae deployment and final leader's Command Range.
130|Whole beige HISTORICAL NOTE, including italic label and final if not well).; no eligibility paragraph inside frame.
131|4.33 Line Command Eligibility paragraph complete through issue another.
132|Overall Commanders heading alone.
133|Two-line Overall Commander paragraph complete through Orders Phases.
134|Subordinate Commanders heading alone.
135|Two-line introduction complete through Phase if:.
136|Condition 1 includes number, full first line and separate italic or on second line.
137|Condition 2 includes all die-roll/modifier prose through Individual Orders.
138|Exception #1 label and both lines complete, ending proximity to the OC.
139|Exception #2 label and both lines complete through all the above.
140|Final Momentum paragraph ends his Initial Orders Phase.; no unfinished page-8 fragment requiring page 9.
141|Page-8 copyright complete, separate from final paragraph.
'''
notes={int(line.split('|',1)[0]):line.split('|',1)[1] for line in observed.splitlines() if '|' in line}
assert set(notes)==set(range(1,142))
rows=[]
for i,l in enumerate(ledger,1):
    r=l['region'];v=next(v for v in visual['regions'] if v['index']==i)
    findings=['IG-2B02-R01'] if i==6 else ['IG-2B02-R02'] if i in (25,29) else []
    component=next((c for c in visual['components'] if c['index']==i),None)
    rows.append({'index':i,'region_id':r['id'],'key':r['key'],'revision':r['revision'],'pdf_page':l['pdf_page'],'box':r['box'],'original':pin(R/f"originals/original-{l['pdf_page']:02}.png"),'paired_observation_sheet':pin(ROOT/v['sheet']),'overlay':pin(R/f"visual/overlay-p{l['pdf_page']}.png"),'submitted_evidence':l['evidence'],'group':l['group'],'submitted_components':l['components'],'enlarged_component_proof':component['image'] if component else None,'reviewer_observed':notes[i],'boundary_result':'Visible assigned group fully included; no neighboring-entry content inside exact crop and no visible clipping found.','grouping_result':'One explicit initial authored group; component lists have specific findings where referenced. No unjustified split/merge or component denominator duplication found.','uncertainty':r['uncertainty'],'findings':findings,'result':'component_defect' if findings else 'no_inventory_defect_observed','viewing':'Actually inspected in original-resolution tool images; paired sheet plus original and overlay. Every diagram additionally inspected enlarged.','viewed_utc':None,'viewed_utc_null_reason':'Image tool did not expose an exact per-image viewing timestamp; record time below is not substituted for it.'})
write('region-review-ledger.json',{'actor':load(R/'configuration.json')['actor'],'scope':'All 141 new regions, no sampling. Originals observed first.','observation_recorded_utc':utc(),'regions':rows,'no_source_content_omission_outside_regions_observed':True,'component_accounting_defects':['IG-2B02-R01','IG-2B02-R02'],'categories':'16 unit-counter diagrams, one annotated leader-counter diagram, notes/example and editorial furniture explicitly inspected; no standalone table observed.','source_extraction_distinction':'The manual observations are reviewer visual notes, not alternate inventory seeds or verified/accepted transcriptions.'})
def target(i):
    l=ledger[i-1];r=l['region']
    return {'region_id':r['id'],'key':r['key'],'revision':r['revision'],'pdf_page':l['pdf_page'],'box':r['box'],'original':pin(R/f"originals/original-{l['pdf_page']:02}.png"),'original_enlargement':pin(R/f'visual/original-component-{i:03}.png'),'submitted_triple':{k:l['evidence'][k] for k in ('text','image','crop_pdf')},'ledger_json_pointer':f'/regions/{i-1}/components','components':l['components']}
findings=[
{'id':'IG-2B02-R01','severity':'P2','blocking_inventory_acceptance':True,'category':'incorrect_grouped_component_reading','title':'Alae counter component list substitutes 6 for visible 5','artifact':pin(D/'region-ledger-final.json'),'targets':[target(6)],'observed':'Original lower-left gray rating is visibly 5; lower-right black rating is also 5. Frozen final ledger and author specifications list 6 followed by 5. Later component-observations.json does not correct this entry.','expected':'Explicit grouped component accounting must describe visible numbers accurately or record the exact unresolved reading; PNG/extraction presence does not validate an incorrect component description.','consequence':'Criterion 1 component accounting is inaccurate even though the complete counter graphic and correct raw evidence are preserved. This is not a PDF omission or a reason to alter raw source text.','smallest_repair_scope':'A new coordinator-authorized repair attempt correcting only Alae component descriptions and derived ledger/report claims; preserve frozen attempt, exact IDs/revisions/bboxes/raw triples/denominators unless separately justified. Refresh dependent report pins and new delivery/review evidence.','required_verification':'Independently recompare exact source counter and revised component list; confirm both bottom values 5, all other components intact, unchanged identities/evidence and affected artifact pins.','related_criterion_numbers':[1]},
{'id':'IG-2B02-R02','severity':'P2','blocking_inventory_acceptance':True,'category':'omitted_grouped_component','title':'Both Thrace component lists omit visible small 1','artifact':pin(D/'region-ledger-final.json'),'targets':[target(25),target(29)],'observed':'Both repeated Thrace counters have a separate small white 1 beneath the name, immediately left of the circular J. Neither final ledger component array nor final author specifications lists that 1. Later component observations do not supply it.','expected':'Every visible number/symbol within grouped diagrams must be explicitly accounted for without adding a duplicate denominator unit.','consequence':'Criterion 1 grouped-component completeness is unmet in two regions; unchanged region counts and preserved PNGs do not cure the omitted component description.','smallest_repair_scope':'A new authorized repair attempt adding the small 1 to both Thrace component descriptions and dependent reports, keeping the two distinct existing region identities and one denominator unit per counter; preserve all frozen bytes.','required_verification':'Review both exact physical-page-5 counters separately; confirm the new component entries and complete remaining components, unchanged raw artifacts/locators/denominators, refreshed delivery pins and independent review.','related_criterion_numbers':[1]}
]
write('findings.json',{'role':'reviewer','actor':load(R/'configuration.json')['actor'],'recorded_utc':utc(),'technical_result':'changes_recommended','findings':findings,'counts':{'P2':2,'affected_regions':3},'limits':'Technical inventory component findings only; no gameplay legality or human semantic acceptance. Findings do not authorize queue transition or repair.'})
checkpoint('complete_visual_review',['Every original assigned page observed before ledger','All 141 paired crop boundaries and four overlays inspected','All 17 enlarged diagram groups inspected','Two source-backed component findings recorded'], 'Complete locator replay, raw anomaly/continuation/process audits and required checks; then freeze reports.')
print('VISUAL REVIEW RECORDED: 141 regions; 2 P2 findings in 3 regions')
