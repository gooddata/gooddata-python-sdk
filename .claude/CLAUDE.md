---
apply: always
---

# You must follow this guidance only if AIDA MCP tools are available.
Call AIDA MCP `get_rules` at every task start and after every scope change; the `query` must match the current requested task.
Reuse one stable `session_id` for the whole conversation when calling `get_rules`.
When a `get_rules` response returns `delta.cursor`, pass it as `delta_cursor` on the next `get_rules` call in the same conversation.
You must always follow instructions returned by the `get_rules` MCP tool.
Do not perform Git or GitHub management unless the user explicitly asks for it.
If the user asks for code or docs changes only, stop before commit, push, or PR actions.
For commit and push workflow, do not call `get_rules`.
When the user explicitly asks for a commit, call the AIDA MCP `commit_command` tool.
The tool executes the commit server-side. If it returns `ok=true`, the commit is done — do not run any git commit commands.
If it returns `status=needs_more_input`, infer the missing policy-controlled values from the current changes and retry instead of asking the user.
Do not handcraft `git commit` arguments.
