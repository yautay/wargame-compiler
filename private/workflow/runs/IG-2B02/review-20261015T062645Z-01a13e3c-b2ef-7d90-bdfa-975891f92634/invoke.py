from review_driver import *
name=sys.argv[1]
if name=='locators':run('09-all-locator-replays',[PY,'-B',R/'locator_replay.py'])
elif name=='visual':run('09-visual-preparation',[PY,'-B',R/'visual_prepare.py'])
elif name=='continuations':run('15-continuation-and-order-audit',[PY,'-B',R/'continuation_audit.py'])
elif name=='process':run('16-generation-process-review',[PY,'-B',R/'process_audit.py'])
elif name=='final-inputs':run('18-final-input-scope-audit',[PY,'-B',R/'final_input_scope_audit.py'])
elif name=='reports':run('16b-report-consistency-audit',[PY,'-B',R/'report_consistency_audit.py'])
elif name=='native-renders':run('19-native-render-audit',[PY,'-B',R/'native_render_audit.py'])
elif name=='replays':
    comparisons=[]
    for n in (1,2):
        destination=R/f'replay-author-{n}'
        assert destination.is_absolute() and not destination.exists() and destination.name!='authored'
        command=run(f'10-author-replay-{n}',[PY,'-B',D/'author.py',destination,D/'authored/identity-registry.json'])
        for f in ('inventory.json','identity-registry.json'):
            actual=pin(destination/f);expected=pin(D/'authored'/f)
            assert actual['sha256']==expected['sha256'] and actual['bytes']==expected['bytes']
            comparisons.append({'expected':expected,'actual':actual,'identical_bytes':True,'command':command})
    write('replay-report.json',{'outcome':'passed','comparisons':comparisons,'registry':pin(D/'authored/identity-registry.json'),'specifications':pin(D/'author-specifications-final.json'),'author_script':pin(D/'author.py'),'safety':'Inspected author.py and ops.py; absolute fresh destinations with basename not authored avoid all executor writes. No UUID allocation or identity reseeding.','identity_bindings':load(D/'authored/identity-registry.json')['entries']})
elif name=='tests':
    import uuid
    basetemp=ROOT/('private/workflow/checks/rv-b02-'+uuid.uuid4().hex[:12]);assert not basetemp.exists()
    run('11-source-tests',[PY,'-B','-m','pytest','-q','tests/sources','--basetemp',basetemp,'-p','no:cacheprovider','--tb=short'])
    run('12-repository-check',[N/'powershell/pwsh.EXE','-NoProfile','-File','scripts/check.ps1','-Task','IG-2B02'])
    run('13-final-workflow-validate',[PY,'-B','scripts/workflow.py','validate'])
    run('14-final-diff-check',['git','diff','--check'])
else:raise ValueError(name)
