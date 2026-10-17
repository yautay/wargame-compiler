import sys,json,subprocess,hashlib,datetime
from pathlib import Path
R=Path(__file__).parent; mode=sys.argv[1]
commands={"sources":[".venv/Scripts/python.exe","-m","pytest","tests/sources","-q","--basetemp",(R/"source-pytest").as_posix(),"-p","no:cacheprovider","--tb=short"],"repository":["pwsh","-NoProfile","-File","scripts/check.ps1","-Task","IG-2B08"],"diff":["git","diff","--check"]}
cmd=commands[mode];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
with (R/f"{mode}.stdout.log").open("xb") as out,(R/f"{mode}.stderr.log").open("xb") as err:c=subprocess.run(cmd,stdout=out,stderr=err)
meta=json.loads((R/"checkpoint.json").read_text()); d={k:meta[k] for k in ["task","role","actor","model","reasoning","configuration_evidence","configuration_sha256"]}; d.update(command=cmd,exit_code=c.returncode,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
for stream in ["stdout","stderr"]:
 p=R/f"{mode}.{stream}.log";d[stream]={"path":p.as_posix(),"sha256":hashlib.sha256(p.read_bytes()).hexdigest(),"bytes":p.stat().st_size}
(R/f"{mode}-execution.json").write_text(json.dumps(d,indent=2)+"\n")
print(json.dumps({"command":cmd,"exit_code":c.returncode,"evidence":(R/f"{mode}-execution.json").as_posix()}))
