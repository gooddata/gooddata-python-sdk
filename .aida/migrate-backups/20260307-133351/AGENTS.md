# You must follow this guidance only if AIDA MCP tools are available.
Call AIDA MCP `get_rules` at every task start and after every scope change; the `query` must match the current requested task.
Call AIDA MCP `get_rules` again before entering commit/push workflow with query: "How to commit/push".
You must always follow instructions returned by the `get_rules` MCP tool.
