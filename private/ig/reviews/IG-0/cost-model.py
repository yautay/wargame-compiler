import json
from pathlib import Path
c,f,d=1000,5,2
result={
 'kind':'illustrative_assumptions_not_observed_operator_cost',
 'clauses':c,'facets_per_clause':f,'relations_per_clause':d,
 'shared_records_K':'excluded; sources/profiles/runs/manifests',
 'atomic_records_excluding_K':c*(5+f+d),
 'clause_records_excluding_K':c*(5+d),
 'semantic_review_targets_both_models':c*(f+d),
 'table_20_by_10':{'cell_nodes':200,'value_assertions':200,'other_records':'excluded'},
 'base_review_hours':[c*2/60,c*5/60],
 'correction_hours':[c*.2*2/60,c*.2*4/60],
 'historical_operator_minutes':None
}
Path('private/ig/reviews/IG-0/cost-model.json').write_text(json.dumps(result,indent=2)+'\n',encoding='utf-8')
print(json.dumps(result,indent=2))
