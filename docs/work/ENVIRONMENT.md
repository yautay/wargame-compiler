# Environment evidence and limitations

Recorded 2026-10-11 for this planning session.

| Item | Requested | Actually confirmed |
|---|---|---|
| Architect | GPT-6 Astra / high | Exact model and reasoning not exposed as trusted session metadata: unknown |
| Future executor | GPT-6.1 Sol / high | Target requirement only; no executor launched |
| Repository | C:\repo\wargame-compiler | Current working directory and PowerShell |
| Python | Existing local environment | .venv/Scripts/python.exe, Python 3.12.14; pytest 9.1.1 |
| Archive destination | C:\repo\wargame-compiler-archive | Absent at inspection; outside writable roots |
| Approval policy | No bypass | never; escalation unavailable in this session |
| Skill installation | Repository-local | .agents is protected read-only; staged skills can be read explicitly |

Do not infer the active model from this prompt, global defaults or the model catalog.
Runtime metadata or the operator's explicit UI observation is needed per execution/review.
No global settings, providers or plugins were changed. No agents, new chats, model runs,
automations or external API calls were made for this preparation.

Local `codex --help` confirms `--model`, `--config`, `--cd`, and `--add-dir` exist.
`--add-dir` changes write scope for a newly configured session; it is not authorization
to escape this session. Installed CLI strings include repo-skill discovery under `.agents`
and `SKILL.md`; this is supporting local evidence, not a successful skill discovery test.
The system skill catalog confirms SKILL.md name/description frontmatter. Repo discovery
and reload must be verified after installation in a permitted session. We did not call
`codex debug prompt-input`, start an app server or infer discovery success from file names.
No new network documentation was fetched under the owner's no-external-API constraint.

Local `rg --help` explicitly documents `.rgignore` and bypass flags. Default `rg --files`
is tested by routine checks. Pytest has explicit testpaths and collection exclusions.
No supported hard model-read deny mechanism was configured or verified here. Markdown
instructions and ignore files are not such mechanisms; the current sandbox permits broad
reads. Context packet allowlists constrain our packet builder only.
