"""Read-only textual inventory for architecture planning, NOT a YAML validator."""
from pathlib import Path
import hashlib
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[4]
OUT = Path(__file__).resolve().parent
GAME = Path('C:/repo/wargame-projects/games/spqr')
WGU = Path('C:/repo/wargame-utils')

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def git(root, *args):
    p = subprocess.run(['git', '-C', str(root), *args], capture_output=True, text=True)
    return {'value': p.stdout.strip() if p.returncode == 0 else None, 'exit_code': p.returncode, 'error': p.stderr.strip()}

files = sorted((GAME / 'kb').rglob('*'))
files = [p for p in files if p.is_file()] + [GAME / 'wgu.yaml']
inventory = [{ 'path': str(p), 'bytes': p.stat().st_size, 'sha256': digest(p)} for p in files]
counts = {}
rules = []
for p in sorted((GAME / 'kb/rules').glob('*.yaml')):
    body = p.read_text(encoding='utf-8-sig')
    chunks = re.split(r'^  - id: ', body, flags=re.M)[1:]
    counts[p.name] = len(chunks)
    rules.extend(chunks)
collections = {}
for name in ['terms', 'tables', 'procedures', 'relations', 'ambiguities', 'changes', 'scenarios']:
    body = (GAME / f'kb/{name}.yaml').read_text(encoding='utf-8-sig')
    body = re.split(r'^' + name + r':\s*$', body, flags=re.M)[1]
    body = re.split(r'^\S', body, maxsplit=1, flags=re.M)[0]
    collections[name] = len(re.findall(r'^  - ', body, re.M))
    if name == 'procedures':
        collections['subprocedures'] = len(re.findall(r'^      - id:', body, re.M))
        collections['steps'] = len(re.findall(r'^\s+- \{n:', body, re.M))
    if name == 'tables':
        collections['tables_complete_true'] = len(re.findall(r'^    complete: true', body, re.M))
    if name == 'relations':
        collections['relations_verified'] = len(re.findall(r'status: verified', body))
    if name == 'terms':
        collections['terms_with_explicit_id'] = len(re.findall(r'^  - (?:\{)?id:', body, re.M))

config = (GAME / 'wgu.yaml').read_text(encoding='utf-8-sig')
source_block = config.split('sources:', 1)[1].split('\ntranslation:', 1)[0]
paths = re.findall(r'\{path:\s*("[^"]+"|[^,}]+)', source_block)
sources = [{'configured_path': p.strip('" '), 'exists': (GAME / p.strip('" ')).is_file()} for p in paths]
manifest = json.loads((ROOT / 'private/archive/poc-2026-10-11/manifest.json').read_text(encoding='utf-8-sig'))
original = 'private/poc/spqr-chapter9/source/original-pdf-20261008-01.pdf'
entry = next(e for e in manifest['entries'] if e['original_path'] == original)
fallback = dict(entry)
fallback['hash_verified'] = digest(ROOT / entry['archive_path']) == entry['sha256']
fallback['binding_to_wgu_original_bytes'] = 'unknown: configured WGU file missing; KB has no original PDF hash'
result = {
    'method': 'Full byte hashing; textual inventory anchored to the observed YAML layout. No YAML parse/schema validation or full semantic review.',
    'game_head': git(GAME, 'rev-parse', 'HEAD'),
    'game_scope_status': git(GAME, 'status', '--short', '--', 'kb', 'wgu.yaml', 'docs'),
    'wgu_head': git(WGU, 'rev-parse', 'HEAD'),
    'wgu_scope_status': git(WGU, 'status', '--short', '--', 'wgu/kb', 'wgu/schemas/kb.schema.json'),
    'files': inventory,
    'rules_by_file': counts,
    'rules_total': len(rules),
    'collections': collections,
    'rules_with_source': sum(bool(re.search(r'^    source:', r, re.M)) for r in rules),
    'rules_with_digital': sum(bool(re.search(r'^    digital:', r, re.M)) for r in rules),
    'configured_sources': sources,
    'archive_source_candidate': fallback,
    'code_basis': [{'path': str(WGU / p), 'sha256': digest(WGU / p)} for p in ['wgu/schemas/kb.schema.json', 'wgu/kb/store.py', 'wgu/kb/export.py', 'wgu/kb/lint.py']],
}
(OUT / 'input-inventory.json').write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
print(json.dumps({k: v for k,v in result.items() if k not in ['files', 'configured_sources', 'code_basis']}, ensure_ascii=False, indent=2))
print('configured sources:', len(sources), 'present:', sum(s['exists'] for s in sources))
