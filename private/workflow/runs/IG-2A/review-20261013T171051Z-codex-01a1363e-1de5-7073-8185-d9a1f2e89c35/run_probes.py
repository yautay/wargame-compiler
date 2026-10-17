from run_checks import OUT, run
import sys
run('boundary-probes-repeat',[sys.executable,str(OUT/'probes.py'),'p2'])
