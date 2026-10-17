import sys,json,subprocess,datetime,time
from pathlib import Path
R=Path(__file__).parent
label=sys.argv[1];args=sys.argv[2:];start=time.monotonic()
p=subprocess.run(args,capture_output=True,text=True,encoding='utf-8',errors='replace')
(R/(label+'.log')).write_text(p.stdout+'\n'+p.stderr,encoding='utf-8')
m=json.loads((R/'review-metadata.json').read_text());m.update(command=subprocess.list2cmdline(args),exit_code=p.returncode,elapsed_seconds=time.monotonic()-start,utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
(R/(label+'.json')).write_text(json.dumps(m,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'check':label,'exit_code':p.returncode,'tail':(p.stdout+'\n'+p.stderr)[-3000:]}));sys.exit(p.returncode)
