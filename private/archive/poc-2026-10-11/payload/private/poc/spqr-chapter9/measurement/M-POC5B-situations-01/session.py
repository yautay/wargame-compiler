import json,pathlib,hashlib,datetime,sys,copy
sys.stdout.reconfigure(encoding='utf-8')
ROOT=pathlib.Path(__file__).resolve().parents[5];P=ROOT/'private/poc/spqr-chapter9';R=P/'reviews/semantic-01';S=P/'reviews/situations-01';M=pathlib.Path(__file__).parent
def read(f):return json.loads(f.read_text(encoding='utf-8-sig'))
def ref(f):
    b=f.read_bytes();return dict(path=f.relative_to(ROOT).as_posix(),bytes=len(b),sha256=hashlib.sha256(b).hexdigest())
def save(f,o):f.write_text(json.dumps(o,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
def md(f,s):f.write_text(s.rstrip()+'\n',encoding='utf-8')
def pointer(o,p):
    for k in p.strip('/').split('/'):
        k=k.replace('~1','/').replace('~0','~');o=o[int(k)] if isinstance(o,list) else o[k]
    return o
now=lambda:datetime.datetime.now(datetime.timezone.utc).isoformat()
RECORD_IDS={
 'SIT-01':['R911'],'SIT-02':['R911'],'SIT-03':['R911','R923'],
 'SIT-04':['R914','N914table'],'SIT-05':['R914','N914table'],
 'SIT-06':['N914table','N914diagram','D914compass','G-D914compass'],
 'SIT-07':['R916','G916'],'SIT-08':['R923','N923ex'],
 'SIT-09':['R922','R931','R932','N932ex'],'SIT-10':['R941'],
 'SIT-11':['R95note','R951','G-D95scenario'],'SIT-12':['R953','G953'],
 'SIT-13':['R962','R963','R964'],'SIT-14':['R966','R968','N966diagram'],
 'SIT-15':['R967','N967ex'],'SIT-16':['R97intro','R971','R972'],
 'SIT-17':['R982','R985','R986','N985markers','N986marker'],
 'SIT-18':['R994','G-D994scenario'],'SIT-19':['R995'],
 'SIT-20':['R996b','R996c','R996d']}

def locate_records(prop,ids):
    result=[]
    for id in ids:
        matches=[(f'/{family}/{idx}',o) for family in ['rules','nodes','dependencies','gaps'] for idx,o in enumerate(prop[family]) if o['id']==id]
        assert len(matches)==1,(id,matches)
        result.append(matches[0])
    return result

def init():
    assert ROOT.as_posix()=='C:/repo/wargame-compiler'
    anchors=read(P/'measurement/M-POC5A-semantic-04d4/preflight.json')['verified']
    for x in anchors:assert ref(ROOT/x['path'])==x
    manifest=read(P/'evaluation/eval-v1/manifest.json')
    for x in manifest['artifacts']:assert ref(ROOT/x['path'])==x
    save(M/'preflight.json',dict(recorded_at_utc=now(),verified=anchors,frozen_evaluation_artifacts=manifest['artifacts'],all_match=True))
    save(M/'immutability-before.json',dict(files=[ref(f) for f in P.rglob('*') if f.is_file() and M not in f.parents],sessions_prefix_only=True))
    situations=read(P/'evaluation/eval-v1/situations.json')['situations'];ids=[x['id'] for x in situations]
    assert ids==[f'SIT-{n:02}' for n in range(1,21)]
    save(M/'estimate.json',dict(recorded_at_utc=now(),before_situation_evaluation=True,card='M-POC5B',minutes_range=[75,90],limit_minutes=90,
       situation_ids=ids,per_answer={'first-001':20,'context-01':20},total_answer_case_judgments=40,
       frozen_situations=ref(P/'evaluation/eval-v1/situations.json'),
       rationale='Twenty frozen local/blocked supplied-fact cases,17local/3blocks. Shared exact source/rule passages with separate original byte traces; inspect all variants, boundaries and conflicts within one90minute part.',
       mode='Manual evaluation of original stored rule representations, not newly elicited scenario answers. Evaluator derivations labelled separately; no engine or inference API.',
       further_split_required=False,active_time='unknown',other_cards_executed=[]))
    print('Original anchors/frozen7artifacts verified; full20cases/40judgments pre-estimated75–90minutes.')

def approve():
    state=read(R/'current-state-30.json');manifest=read(R/'part-04d5/manifest.json')
    for x in manifest['artifacts']:assert ref(ROOT/x['path'])==x
    evidence=dict(owner_reply_verbatim='zatwierdzam i kontynuuj',message_sent_at_utc='unknown',recorded_at_utc=now(),
       presentation=ref(R/'part-04d5/presentation.json'),owner_focus=ref(R/'part-04d5/owner-focus.md'),
       interpretation='Owner accepts immediately preceding exact .4d5 reconciliation recommendation and transfer to M-POC5B with older8pending/13issues preserved. No new meaning variant, whole-record or full-metric acceptance.',owner_file_open_or_read='unknown')
    save(M/'approval-evidence.json',evidence)
    assert not (R/'owner-decision-15.json').exists()
    decision=dict(id='M-POC5A-owner-decision-15',card='M-POC5A',part='M-POC5A.4d5',date='2026-10-11',timezone='Europe/Warsaw',recorded_at_utc=now(),
       owner_reply_verbatim='zatwierdzam i kontynuuj',reviewer='owner in this chat; personal identity unknown',approval_evidence=ref(M/'approval-evidence.json'),
       decision='accepted_exact_reconciliation_and_bounded_transfer_to_M_POC5B',comparison_manifest=ref(R/'part-04d5/manifest.json'),
       reconciliation_scope=state['summary'],prior_decision=state['decision'],prior_state=ref(R/'current-state-30.json'),evaluation=state['evaluation'],responses=state['responses'],
       accepted_recommendation='REC-4D5-01',new_inventory_judgments=0,new_rule_points=0,previous_inventory_owner_decisions=414,
       pending_expectation_ids=state['pending_expectation_ids'],unresolved_issue_ids=state['unresolved_issue_ids'],
       excluded=['Old pending variants, whole records/fields, real map/scenario/rating/table values, full quality/precision/recall and future situation judgments.'],
       owner_file_open_or_read='unknown',M_POC5A_whole_closed=False,full_metrics='not_assessable',no_new_sources=True,no_extraction_or_correction=True)
    save(R/'owner-decision-15.json',decision)
    overlay=read(R/'owner-review-overlay-14.json');overlay.update(id='M-POC5A-owner-review-overlay-15',decision=ref(R/'owner-decision-15.json'),
       prior_overlay=ref(R/'owner-review-overlay-14.json'),reconciliation_owner_decision=ref(R/'owner-decision-15.json'),
       reconciliation_report=ref(R/'part-04d5/manifest.json'),reconciliation_scope_accepted=True,no_new_rule_points_from_reconciliation=True)
    save(R/'owner-review-overlay-15.json',overlay)
    s=copy.deepcopy(state);s.update(id='M-POC5A-current-state-31',part='M-POC5A.4d5-owner-review',previous_state=ref(R/'current-state-30.json'),
       decision=ref(R/'owner-decision-15.json'),overlay=ref(R/'owner-review-overlay-15.json'),part_4d5_owner_reconciliation_complete=True,
       part_4d5_reconciliation_pending=False,new_owner_decisions=[ref(R/'owner-decision-15.json')],next_part='M-POC5B',
       next_action='Execute fullM-POC5B20frozen situations in both original representations after fresh75–90minute estimate. Preserve old8expectations/13issues.',
       resume='Exact .4d5 reconciliation approved.414inventory decisions and old8pending/13issues retained. M-POC5B starts in this new evaluating session.')
    s['summary']['owner_reconciliation_status']='accepted_exact_reconciliation';s['reconciliation_counts'].update(owner_decided_packages=1,pending_packages=0)
    save(R/'current-state-31.json',s)
    md(R/'owner-review-summary-15.md','''# Zatwierdzenie uzgodnienia .4d5

Właściciel: „zatwierdzam i kontynuuj”. Przyjęto dokładne uzgodnienie .4d5 i przekazanie do M-POC5B z ograniczeniami.414 wcześniejszych ocen inwentarza,257 zakresów relacji,124 lokatory i264 pary rubryki zachowane; nowych punktów0. Starsze8 oczekiwań/13 kwestii pozostają otwarte, pełne metryki nieocenialne. Zgoda nie przyjmuje jeszcze wyników20 sytuacji.
''')
    print('Owner-decision/overlay15 and current-state31 saved; .4d5 reconciliation accepted, old8/13 preserved.')

def show(start,end):
    situations=read(P/'evaluation/eval-v1/situations.json')['situations']
    byrun={run:read(P/f'proposals/{run}/proposal.json') for run in ['first-001','context-01']}
    seen={run:set() for run in byrun}
    for s in situations[start:end]:
        print('\nCASE',json.dumps({k:s[k]for k in ['id','facts','question','expected','expectation_ids','dependency_ids']},ensure_ascii=False))
        print('SOURCE exact child before envelope:')
        for e in s['evidence']:print(e['pdf_page'],e['column'],e.get('source_span',e.get('source_transcription',e.get('transcription','graphic'))))
        for run,prop in byrun.items():
            print('ANSWER',run)
            for ptr,rec in locate_records(prop,RECORD_IDS[s['id']]):
                if ptr in seen[run]:print(ptr,'same exact original record already displayed in this batch; independently apply current case facts.');continue
                seen[run].add(ptr)
                if ptr.startswith('/dependencies/'):
                    print(ptr,json.dumps({k:rec[k]for k in ['id','from','to','kind','target_status','impact_if_missing','gap_ids']},ensure_ascii=False))
                elif ptr.startswith('/gaps/'):
                    print(ptr,json.dumps(rec,ensure_ascii=False))
                else:
                    print(ptr,json.dumps({k:(v.get('value') if isinstance(v,dict) and 'state'in v else v) for k,v in rec.items()
                       if k in ['id','transcription','interpretation','conditions','action_effect','exceptions','parameters','time_limits','content','gap_ids']},ensure_ascii=False))

if __name__=='__main__':
    if sys.argv[1]=='init':init()
    elif sys.argv[1]=='approve':approve()
    elif sys.argv[1]=='show':show(int(sys.argv[2]),int(sys.argv[3]))
