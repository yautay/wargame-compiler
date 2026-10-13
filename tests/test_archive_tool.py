"""Exercise relocation on synthetic data only. Real archive auditing is explicit."""
import json
from pathlib import Path
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]

def setup(tmp_path):
    repo=tmp_path/'repo'; (repo/'scripts').mkdir(parents=True)
    shutil.copyfile(ROOT/'scripts/archive.ps1',repo/'scripts/archive.ps1')
    (repo/'private/workflow').mkdir(parents=True)
    for folder in ['archive','private/archive','docs/adr','docs/reviews','private/ig/migration',
                   'private/ig/research','private/ig/reviews','private/ig/_checks']:
        p=repo/folder; p.mkdir(parents=True,exist_ok=True)
        (p/'fixture.bin').write_bytes(b'\x00\xffunchanged historical bytes\r\n')
        (p/'empty').mkdir()
    for rel in ['docs/prompts/IG-0-critical-review.md','docs/work/tasks/IG-0.md']:
        p=repo/rel; p.parent.mkdir(parents=True,exist_ok=True); p.write_bytes(b'Historical text\r\n')
    return repo,tmp_path/'external'

def run(repo,external,mode,*args):
    return subprocess.run(['pwsh','-NoProfile','-File',str(repo/'scripts/archive.ps1'),
                           '-Mode',mode,'-ArchiveRoot',str(external),*args],cwd=repo,
                          capture_output=True,text=True,timeout=60)

def test_copy_verify_restore_then_remove_exact_sources(tmp_path):
    repo,external=setup(tmp_path)
    original=(repo/'archive/fixture.bin').read_bytes()
    r=run(repo,external,'Inventory'); assert r.returncode==0,r.stderr
    r=run(repo,external,'VerifySource'); assert r.returncode==0,r.stderr
    manifest=json.loads((repo/'private/workflow/relocation.json').read_text(encoding='utf-8-sig'))
    r=run(repo,external,'Migrate','-RemoveVerifiedSources'); assert r.returncode==0,r.stderr
    assert not (repo/'archive').exists()
    r=run(repo,external,'VerifyExternal'); assert r.returncode==0,r.stderr
    restore=tmp_path/'restored'
    r=run(repo,external,'Restore','-RestoreRoot',str(restore)); assert r.returncode==0,r.stderr
    assert (restore/'archive/fixture.bin').read_bytes()==original
    assert (restore/'private/archive/empty').is_dir()
    report=json.loads((external/manifest['batch']/'verification.json').read_text(encoding='utf-8-sig'))
    assert report['restored'] and report['sources_removed'] and report['files']==10
    r=run(repo,external,'Restore','-RestoreRoot',str(restore)); assert r.returncode!=0
    entry=manifest['entries'][0]; (external/entry['new_path']).write_bytes(b'Corrupted copy')
    r=run(repo,external,'VerifyExternal'); assert r.returncode!=0

def test_source_change_aborts_before_copy_or_delete(tmp_path):
    repo,external=setup(tmp_path)
    assert run(repo,external,'Inventory').returncode==0
    p=repo/'archive/fixture.bin'; p.write_bytes(b'Changed after inventory')
    result=run(repo,external,'Migrate','-RemoveVerifiedSources')
    assert result.returncode!=0 and p.read_bytes()==b'Changed after inventory'
    assert not external.exists()

def test_existing_external_batch_is_never_overwritten(tmp_path):
    repo,external=setup(tmp_path)
    assert run(repo,external,'Inventory').returncode==0
    m=json.loads((repo/'private/workflow/relocation.json').read_text(encoding='utf-8-sig'))
    batch=external/m['batch']; batch.mkdir(parents=True)
    sentinel=batch/'keep'; sentinel.write_bytes(b'Existing archive')
    result=run(repo,external,'Migrate','-RemoveVerifiedSources')
    assert result.returncode!=0 and sentinel.read_bytes()==b'Existing archive'
    assert (repo/'archive/fixture.bin').exists()
