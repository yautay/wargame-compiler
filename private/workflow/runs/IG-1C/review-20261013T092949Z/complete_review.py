"""Complete append-only packaging after a missing optional empty project log."""
from pathlib import Path
import json
from datetime import datetime, timezone
import hashlib

run = Path(__file__).resolve().parent
original = run / 'freeze_review.py'
code = original.read_text(encoding='utf-8')

def transform(old, new):
    global code
    assert code.count(old) == 1, old
    code = code.replace(old, new)

transform("def write(name, value):\n    with", "def write(name, value):\n    if (RUN / name).exists():\n        assert load(RUN / name) == value, 'Preserve earlier generated evidence: ' + name\n        return\n    with")
transform("write('measurements.json', measurements)", "measurements = load(RUN / 'measurements.json')\nwrite('measurements.json', measurements)")
transform("with (RUN / 'report.md').open('x', encoding='utf-8', newline='\\n') as stream:\n    stream.write(report)", "assert (RUN / 'report.md').read_text(encoding='utf-8') == report, 'Preserve prior generated report bytes'")
transform("['plan.log', 'dry-run.log', 'pytest.log', 'diff-check.log', 'result.json']", "['plan.log', 'dry-run.log', 'pytest.log', 'result.json']")
completed = datetime.now(timezone.utc)
root = run.parents[4]
record = {'end_utc': completed.isoformat(), 'start_utc': '2026-10-13T09:29:49+00:00', 'wall_seconds': (completed - datetime.fromisoformat('2026-10-13T09:29:49+00:00')).total_seconds(), 'interval': 'Resumed independent review including append-only evidence-packaging correction; excludes earlier configuration/queue waiting.', 'preserved_packaging_script_sha256': hashlib.sha256(original.read_bytes()).hexdigest(), 'input_tokens': None, 'output_tokens': None, 'cost': None, 'operator_time_seconds': None, 'product_repair_cycles': 0}
with (run / 'completion-measurements.json').open('x', encoding='utf-8') as stream:
    json.dump(record, stream, indent=2)
    stream.write('\n')
transform("'measurements': measurements,", "'measurements': measurements, 'completion_measurements': load(RUN / 'completion-measurements.json'),")
exec(compile(code, str(original), 'exec'), {'__file__': str(original), '__name__': '__main__'})
