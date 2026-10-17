"""Verify preserved harness with exact json.loads(literal) schema encoding."""
from pathlib import Path

original = Path(__file__).with_name('verify.py')
source = original.read_text(encoding='utf-8')
old = "embedded = next(ast.literal_eval(n.value) for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'WGU_SCHEMA' for t in n.targets))"
new = """assignment = next(n.value for n in tree.body if isinstance(n, ast.Assign) and any(isinstance(t, ast.Name) and t.id == 'WGU_SCHEMA' for t in n.targets))
assert isinstance(assignment, ast.Call) and isinstance(assignment.func, ast.Attribute)
assert isinstance(assignment.func.value, ast.Name) and assignment.func.value.id == 'json' and assignment.func.attr == 'loads'
assert len(assignment.args) == 1 and not assignment.keywords
embedded_literal = ast.literal_eval(assignment.args[0])
assert isinstance(embedded_literal, str)
embedded = json.loads(embedded_literal)"""
assert source.count(old) == 1
exec(compile(source.replace(old, new), str(original), 'exec'), {'__file__': str(original), '__name__': '__main__'})
