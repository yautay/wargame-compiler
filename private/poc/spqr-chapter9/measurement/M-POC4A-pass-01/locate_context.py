"""Prepare source locators and cost decision BEFORE materializing the context."""
import re
import collections
import datetime
import pdfplumber
from prepare import ROOT, P, M, load, desc, save

src=P/'source/original-pdf-20261008-01.pdf'
index=collections.defaultdict(list)
with pdfplumber.open(src) as pdf:
    for n,page in enumerate(pdf.pages,1):
        for column,box in [('left',(40,40,300,745)),('right',(310,40,575,745))]:
            # Locator candidates only: first word on a text line, excluding the index.
            if n>=42: continue
            for line in page.crop(box).extract_text_lines():
                match=re.match(r'^(\d{1,2}\.\d{1,2})\s',line['text'])
                if match:
                    index[match[1]].append(dict(pdf_page=n,column=column,
                        bbox_pdf_points=[line['x0'],line['top'],line['x1'],line['bottom']],
                        heading_line=line['text'],status='helper_heading_locator_candidate'))
    crop=pdf.pages[26].crop((40,413,300,650))
    selected_text=crop.extract_text()
    selected_chars=[dict(text=c['text'],x0=c['x0'],top=c['top'],x1=c['x1'],bottom=c['bottom']) for c in crop.chars]

save(M/'source-locator-index.json',dict(source=desc(src),numbering='one-based PDF physical pages',
    search_scope='44-page verified PDF; body heading scan pages 1-41, index excluded; source lookup only, not an extraction input',
    semantic_acceptance='not_performed',rule_heading_candidates=dict(index)))

def locate(label):
    tokens=re.findall(r'\b\d{1,2}\.\d{1,2}\b',label)
    candidates=[]
    for token in tokens:
        candidates += [dict(rule=token,**r) for r in index.get(token,[])]
    return candidates

budget=dict(id='M-POC4A-pass-01-pre-expansion',recorded_at_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
    baseline_extra_pages=0, baseline_context_responses=0,
    proposed_unique_additional_pdf_pages=[27],proposed_unique_additional_rule_ids=['8.46'],
    proposed_additional_table_ids=[], counts=dict(pages=1,rules=1,tables=0,selected_dependency_depth=1,
        longest_considered_path_depth=2,prepared_passes=1,inference_rounds=0,reserved_rounds=1),
    paths=[dict(nodes=['9.32','8.46/Step-4'],depth=1,status='selected'),
           dict(nodes=['9.32','8.46/Step-4','CTX-TBL-SHOCK-CRT'],depth=2,status='blocked_source')],
    limits=dict(pages=8,rules=20,tables=4,depth=2,rounds=2),first_reached_limit_applies=True,
    stop=dict(first_reached_limit='dependency_depth',at_depth=2,
        action='Do not recursively extend targets reached at depth 2. Missing CRT stays blocked; no implicit third step or pass-02.'),
    rationale='Existing requires_context EXP-031 and declarations G932/G-D932CRT ask for the numerical AS/LC procedure. Select only 8.46 Step 4; do not acquire unrelated ordinary procedures for synthetic local tests.',
    scope_rule='Rule counted once even for a partial clause; shared page once; references are not supplied rules or tables. Full reviewer renders remain outside extractor allowlist.',
    remaining_headroom=dict(pages=7,rules=19,tables=4,depth=0,rounds_after_reserved=1),
    active_user_time='unknown',active_model_time='unknown',remaining_active_budget='unknown',
    time_budget_compliance='unknown',scope_limit_compliance=True,
    decision='prepare_for_human_review_only; do not infer budget compliance or dispatch inference')
save(M/'pre-expansion-budget.json',budget)
save(M/'selected-source-locator.json',dict(source=desc(src),rule='8.46',fragment='Step 4: Apply Results',
    pdf_page=27,column='left',bbox_pdf_points=[40,413,300,650],
    parent_heading=locate('8.46'),helper_text=selected_text,glyphs=selected_chars,
    status='awaiting_visual_check',scope='Complete Step 4 including all four bullets and final 10.13 reference; no Step 1-3 or 8.47 supplied.'))
print('PRE-EXPANSION:',budget['counts'])
print('8.46 heading:',locate('8.46'))
print('EXCERPT:',selected_text)
