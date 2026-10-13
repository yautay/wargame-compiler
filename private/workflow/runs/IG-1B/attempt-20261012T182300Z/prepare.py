"""Explicit read-only input enumeration for IG-1B readiness."""
import hashlib
import json
import os
import stat
from datetime import datetime, timezone
from pathlib import Path

HERE = Path(__file__).parent
GAME = Path('C:/repo/wargame-projects/games/spqr')


def check_chain(path):
    for part in [*reversed(path.parents), path]:
        try:
            info = part.lstat()
        except FileNotFoundError:
            break
        if stat.S_ISLNK(info.st_mode) or getattr(info, 'st_file_attributes', 0) & 1024:
            raise ValueError('Linked input: ' + str(part))


def pin(path):
    return {'path': path.absolute().relative_to(Path.cwd()).as_posix(),
            'sha256': hashlib.sha256(path.read_bytes()).hexdigest()}


files = [GAME / 'wgu.yaml']
check_chain(GAME / 'kb')
for directory, dirs, names in os.walk(GAME / 'kb', followlinks=False):
    for name in dirs + names:
        check_chain(Path(directory) / name)
    files += [Path(directory) / name for name in names]
items = []
for path in sorted(files, key=lambda p: p.relative_to(GAME).as_posix()):
    check_chain(path)
    raw = path.read_bytes()
    items.append({'relative_path': path.relative_to(GAME).as_posix(),
                  'role': 'game_config' if path == GAME / 'wgu.yaml' else 'kb',
                  'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
old = json.loads(Path('private/ig/planning/wgu-spqr-2026-10-11/input-inventory.json').read_text(encoding='utf-8'))
configured = []
for item in old['configured_sources']:
    path = GAME / item['configured_path']
    check_chain(path)
    try:
        info = path.lstat()
        availability = 'available' if stat.S_ISREG(info.st_mode) else 'not_regular'
    except FileNotFoundError:
        availability = 'missing'
    configured.append({'relative_path': item['configured_path'], 'role': 'configured_source',
                       'availability': availability})
registry = Path('private/ig/sources/spqr-5e')
sources = []
for name in ['provenance.json', 'rulebook.pdf']:
    path = registry / name
    check_chain(path.absolute())
    raw = path.read_bytes()
    sources.append({'relative_path': name, 'role': 'provenance' if name.endswith('.json') else 'selected_rulebook',
                    'bytes': len(raw), 'sha256': hashlib.sha256(raw).hexdigest()})
request = {'task': 'IG-1B', 'game_root': GAME.as_posix(), 'game_files': items,
           'historical_configured_sources': configured, 'registry_root': registry.absolute().as_posix(),
           'registry_files': sources,
           'selection': {'source_id': 'spqr-5e-rulebook', 'role': 'rulebook', 'edition_label': '5E',
                         'edition_basis': 'Operator-assigned promoted SPQR 5E registry; source text is not semantically reviewed',
                         'selected_path': 'rulebook.pdf', 'sha256': sources[1]['sha256'],
                         'identity_to_wgu_original': 'unknown', 'semantic_acceptance': 'not_granted'},
           'enumerated_utc': datetime.now(timezone.utc).isoformat(),
           'enumeration_scope': 'Exactly wgu.yaml and regular files in kb/; no other game directories or WGU utility repository. The 36 historical configured source paths are checked individually for availability only at preflight. Registry reads: exactly provenance.json and rulebook.pdf.',
           'auxiliary_policy': 'Any additional auxiliary input needs explicit enumeration; no inferred source reads.'}
(HERE / 'input-request.json').write_text(json.dumps(request, indent=2) + '\n', encoding='utf-8')
prior = {Path(f['path']).relative_to(GAME).as_posix(): f['sha256'] for f in old['files']}
comparison = {'current_count': len(items), 'prior_game_file_count': len(prior),
              'added_paths': [f['relative_path'] for f in items if f['relative_path'] not in prior],
              'changed_paths': [f['relative_path'] for f in items if f['relative_path'] in prior and f['sha256'] != prior[f['relative_path']]],
              'removed_paths': sorted(set(prior) - {f['relative_path'] for f in items}),
              'configured_source_count': len(configured),
              'configured_availability': {v: sum(x['availability'] == v for x in configured) for v in {x['availability'] for x in configured}},
              'source_hash_matches_provenance': sources[1]['sha256'] == json.loads((registry / 'provenance.json').read_text(encoding='utf-8'))['sha256'],
              'owned_paths': {p: Path(p).exists() for p in ['src/wgc/inputs', 'tests/inputs', 'private/ig/projects/spqr/inputs', 'private/ig/projects/spqr/sources', 'contracts/ig/input.schema.json']}}
(HERE / 'preflight.json').write_text(json.dumps(comparison, indent=2) + '\n', encoding='utf-8')
ready = {'role': 'coordinator', 'actor': 'coordinator-20261012T181945Z',
         'summary': 'IG-1A done; IG-1B exact input scope and current hashes pinned. Promoted PDF selection explicit, identity to WGU original unknown. Missing auxiliary sources do not block available KB snapshot. Operator authorized next task.',
         'criteria': ['IG-1A dependency done', 'Exact read/write scope and input revisions pinned', 'No unresolved task refinement'],
         'artifacts': [pin(HERE / 'input-request.json'), pin(HERE / 'preflight.json'), pin(Path('private/workflow/runs/IG-1A/acceptance-20261012T181945Z/completion.json'))],
         'model': 'gpt-6.1-sol', 'reasoning': 'high',
         'configuration_evidence': pin(Path('private/workflow/runs/IG-1A/review-handoff-20261012T180728Z/configuration.json'))}
(HERE / 'ready.json').write_text(json.dumps(ready, indent=2) + '\n', encoding='utf-8')
print(json.dumps(comparison, indent=2))
