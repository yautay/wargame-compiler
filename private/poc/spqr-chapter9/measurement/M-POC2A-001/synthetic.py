"""Author a fictional format illustration, never an extraction response."""
from prepare import P, write
import hashlib

text = 'K.1 During movement, an active Scout may move at most 2 cells once per turn unless a storm is active. Resolve gate entry using Gate table G.'
source_hash = hashlib.sha256(text.encode('utf-8')).hexdigest()

def field(value=None, state='known', evidence=None, reason=None, gaps=None):
    return {'state': state, 'value': value, 'evidence_ids': evidence if evidence is not None else ['S-E1'], 'reason': reason, 'gap_ids': gaps or []}

def rule(rid, cid, transcription, conditions, effect, exceptions, parameters, types, time, gaps):
    return {'id': rid, 'original_label': field('K.1'), 'scope_role': 'core', 'clause_map': [{'local_clause_id':cid,'region_id':'synthetic-core','evidence_ids':['S-E1'],'original_label_text':'K.1'}], 'transcription': field(transcription), 'interpretation': field(effect), 'conditions':field(conditions), 'action_effect':field(effect), 'exceptions':exceptions, 'parameters':parameters, 'unit_types':field(types), 'scope_limits':field(['Fictional movement clause; not a complete game specification']), 'time_limits':time, 'evidence_ids':['S-E1'], 'gap_ids':gaps, 'review_status':'unreviewed'}

example = {
    'format_version':'proposal-format-v1', 'run_id':'synthetic-example-only',
    'input_manifest_sha256':'unknown', 'evaluation_id':'not_applicable_synthetic',
    'scope':{'source_id':'SYNTHETIC-ONLY','source_sha256':source_hash,'pdf_pages':[1],'core_boundaries':'synthetic-core: whole embedded fictional paragraph','boundary_context':[]},
    'provenance':{'application':'authored synthetic format illustration','actual_model_visible_name':'unknown','reasoning_level':'unknown','metadata_source':'No extraction session claimed','assessment_exposure':'not_applicable_synthetic','manifest_hash_reason':'No input manifest exists for the embedded fictional example'},
    'sources':[{'id':'SYNTHETIC-ONLY','sha256':source_hash,'embedded_utf8_text':text}],
    'evidence':[{'id':'S-E1','source_id':'SYNTHETIC-ONLY','source_sha256':source_hash,'pdf_page':1,'printed_page':'1','region_id':'synthetic-core','kind':'text','quote':{'state':'known','value':text,'evidence_ids':[],'reason':'Exact embedded fictional source; not a real PDF','gap_ids':[]},'image':None}],
    'nodes':[],
    'rules':[
        rule('S-R1','S-C1',text.split(' Resolve')[0],['active Scout','movement phase'],'Scout may move at most 2 cells',field(['storm active prevents this permission']),field([{'name':'movement maximum','value':2,'unit':field('cell'),'evidence_ids':['S-E1']}]),['Scout'],field(['during movement','once per turn']),[]),
        rule('S-R2','S-C2','Resolve gate entry using Gate table G.', ['gate entry'],'Use Gate table G; resolution outcome unavailable',field([],state='established_absent',reason='No exception is stated in this fictional gate-entry clause; external table exceptions remain unknown'),field(state='unknown',reason='Referenced table is not supplied',gaps=['S-G1']),['Scout'],field(state='unknown',reason='Timing of Gate table resolution is not supplied',gaps=['S-G1']),['S-G1'])
    ],
    'dependencies':[{'id':'S-D1','from':'S-R2','to':None,'target_candidate':{'original_reference':'Gate table G','description':'Referenced gate-entry resolution table','needed_context':'Gate table G, including headings and notes'},'kind':'table_use','explicitness':'explicit','rationale':'The gate-entry clause explicitly directs the player to use the table; direction is user clause to used table.','evidence_ids':['S-E1'],'target_status':'unresolved','impact_if_missing':{'affected_ids':['S-R2'],'blocks_full_result':True,'reason':'Actual gate-entry result cannot be determined'},'gap_ids':['S-G1'],'review_status':'unreviewed'}],
    'gaps':[{'id':'S-G1','class':'missing_context','affected_ids':['S-R2','S-D1'],'source_regions':['synthetic-core'],'reason':'Gate table G is referenced but absent from the fictional input','needed_context':'Gate table G and its timing/parameters/notes','blocking':True,'evidence_ids':['S-E1']}],
    'coverage':{'core_regions':[{'region_id':'synthetic-core','status':'represented','rule_ids':['S-R1','S-R2'],'node_ids':[],'dependency_ids':['S-D1'],'gap_ids':['S-G1'],'notes':'One label split into movement permission and gate-resolution clauses; result of referenced table remains unknown.'}], 'observed_objects':[{'kind':'rule_label','original_label':'K.1','rule_ids':['S-R1','S-R2'],'clause_ids':['S-C1','S-C2']}], 'boundary_context_regions':[], 'empty_collection_reasons':{'nodes':'No target content is supplied; table remains an explicit unresolved candidate.'}}
}
write(P / 'formats/synthetic-example-v1.json', example)
print('Fictional example authored; no SPQR content or extraction response')
