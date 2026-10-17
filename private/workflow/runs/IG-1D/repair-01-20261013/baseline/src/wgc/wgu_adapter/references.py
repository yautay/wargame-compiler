"""Exact navigational/candidate endpoints; unresolved scopes and legal graph cycles."""
from __future__ import annotations

from collections import defaultdict
import re

from wgc.contracts.source import canonical_bytes


def _cycles(edges):
    """Iterative components are diagnostics, never a rule/procedure DAG requirement."""
    graph=defaultdict(set)
    for a,b in edges:graph[a].add(b);graph.setdefault(b,set())
    visited=set();order=[]
    for node in sorted(graph):
        stack=[(node,False)]
        while stack:
            member,exiting=stack.pop()
            if exiting:order.append(member);continue
            if member in visited:continue
            visited.add(member);stack.append((member,True))
            stack.extend((target,False) for target in reversed(sorted(graph[member])) if target not in visited)
    reverse=defaultdict(set)
    for node,targets in graph.items():
        reverse.setdefault(node,set())
        for target in targets:reverse[target].add(node)
    visited=set();components=[]
    for node in reversed(order):
        if node in visited:continue
        stack=[node];members=[]
        while stack:
            member=stack.pop()
            if member in visited:continue
            visited.add(member);members.append(member);stack.extend(sorted(reverse[member]-visited))
        if len(members)>1 or node in graph[node]:components.append(sorted(members))
    return sorted(components)


def diagnose(reconciled, *, scope_resolutions=None):
    """Caller scope decisions need exact current targets and a recorded basis.

    Stored aliases may resolve only when unique among active identities. No wildcard
    expansion or subpoint-to-base substitution is inferred. Refs/see are navigation;
    WGU relation endpoints remain unaccepted typed candidates.
    """
    scope_resolutions=scope_resolutions or {}
    registry=reconciled['registry']
    active={e['id']:e for e in registry['entries'] if e['active']}
    external=defaultdict(set)
    for identity,e in active.items():
        for alias in e['external_ids']:external[alias].add(identity)
    assignments={a['locator']:a for a in reconciled['assignments']}
    for raw,decision in scope_resolutions.items():
        targets=decision.get('targets',[])
        if (not isinstance(raw,str) or not raw or not decision.get('basis') or not targets
                or len(targets)!=len(set(targets))):
            raise ValueError('scope resolution requires distinct exact targets and basis')
        for target in targets:
            if target not in active and len(external.get(target,set()))!=1:
                raise ValueError('scope resolution target is not uniquely current')
    def endpoint(raw):
        if raw in scope_resolutions:
            decision=scope_resolutions[raw]
            targets=sorted({t if t in active else next(iter(external[t])) for t in decision['targets']})
            return {'target_status':'resolved','target_ids':targets,'candidate_ids':[],
                    'scope_status':'explicit_exact_set','basis':decision['basis']}
        candidates=sorted(external.get(raw,set()))
        if len(candidates)==1:
            return {'target_status':'resolved','target_ids':candidates,'candidate_ids':[],
                    'scope_status':'exact_identifier','basis':'Unique persisted declared identifier/alias'}
        if candidates:
            return {'target_status':'ambiguous','target_ids':[],'candidate_ids':candidates,
                    'scope_status':'identifier_collision','basis':'No candidate selected'}
        if '*' in raw or raw.endswith('.x'):
            status='unresolved_scope'
        elif re.search(r'\d[a-z]+$',raw):
            status='unresolved_subpoint'
        else:status='unresolved_identifier_or_text'
        return {'target_status':'unresolved','target_ids':[],'candidate_ids':[],
                'scope_status':status,'basis':'No exact justified current target; raw locator retained'}
    diagnostics=[];edges=[]
    for r in reconciled['records']:
        owners=assignments[r['locator']]['ids'];value=r['value']
        if not isinstance(value,dict):continue
        declarations=[]
        for field in ('refs','see'):
            if field not in value:continue
            raw=value[field]
            if field=='refs' and isinstance(raw,list):
                declarations.extend((field+'/'+str(i),v,'navigation') for i,v in enumerate(raw) if isinstance(v,str))
            elif isinstance(raw,str):declarations.append((field,raw,'navigation'))
        if r['kind']=='relation':
            declarations.extend((k,value[k],'relation_candidate') for k in ('from','to') if isinstance(value.get(k),str))
        by_field={}
        for field,raw,role in declarations:
            result=endpoint(raw) if raw else {'target_status':'unresolved','target_ids':[],
                'candidate_ids':[],'scope_status':'empty_locator','basis':'Empty text proves no absence'}
            d={'owner_ids':owners,'origin':r['origin'],'field':field,'raw_locator':raw,
               'role':role,'semantic_acceptance':'not_granted',**result}
            diagnostics.append(d);by_field[field]=result
            if role=='navigation':
                edges.extend((owner,t) for owner in owners for t in result['target_ids'])
        if r['kind']=='relation' and all(k in by_field for k in ('from','to')):
            edges.extend((a,b) for a in by_field['from']['target_ids'] for b in by_field['to']['target_ids'])
    return {'format':'wgc-reference-report-1','diagnostics':sorted(diagnostics,key=canonical_bytes),
            'cycles':_cycles(edges),'cycles_are_allowed':True,
            'semantic_acceptance':'not_granted','executable_readiness':'not_granted'}
