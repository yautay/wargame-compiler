# Repository skills

Three concise skills are authored under [docs/skills](../skills/):

- [wgc-queue](../skills/wgc-queue/SKILL.md): select/refine tasks, coordinate handoffs and blockers.
- [wgc-execute](../skills/wgc-execute/SKILL.md): one scoped implementation and frozen delivery.
- [wgc-review](../skills/wgc-review/SKILL.md): independent review and acceptance evidence.

They were prepared using the installed skill-creator instructions. Frontmatter and
references are checked locally. The supported Codex repository convention to verify
in the target session is `.agents/skills/<name>/SKILL.md`; the installed CLI contains
repo skill discovery, but end-to-end discovery has not been run here. This session
marks `.agents` read-only, so these are **staged, not auto-discovered** skills.
Explicitly read the linked SKILL.md in the launch prompts; this works without installation.

In a session with permission to write `.agents`, the operator can copy each staged
directory into `.agents/skills/` without overwriting an existing skill, then start/reload
Codex and verify the three names appear in its skill list. Revalidate links because the
instructions use repository-root paths, not relative paths into docs. No global install,
plugin or user configuration is needed. Keep docs/skills as the source and compare copies
before updating them; do not maintain divergent instruction sets.

Actual discovery in this environment remains an installation check, not a claimed result.

The installed skill-creator `quick_validate.py` was attempted for all three skills but
cannot import PyYAML in either available Python runtime. No network installation was
attempted. Local tests check the deliberately simple name/description frontmatter,
names, required files and absence of scaffold placeholders; manual checks cover routing
and authority boundaries. This is not a claim that the bundled validator passed.
