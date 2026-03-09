---
apply: always
---

# You must follow this guidance only if AIDA MCP tools are available.
Call AIDA MCP `get_rules` at every task start and after every scope change; the `query` must match the current requested task.
You must always follow instructions returned by the `get_rules` MCP tool.
For commit and push workflow, do not call `get_rules`.
Before any commit, call the AIDA MCP `commit_command` tool and execute the returned raw `git commit` command exactly.
Do not handcraft `git commit` arguments or rewrite the returned command.
