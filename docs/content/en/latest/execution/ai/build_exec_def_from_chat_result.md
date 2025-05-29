---
title: "build_exec_def_from_chat_result"
linkTitle: "build_exec_def_from_chat_result"
weight: 95
superheading: "compute."
---

``build_exec_def_from_chat_result(chat_result: ChatResult) -> ExecutionDefinition``

Build execution definition from chat result.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="chat_result" p_type="ChatResult" >}}
ChatResult object containing visualization details from AI chat response
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_name="execution_definition" p_type="ExecutionDefinition" >}}
ExecutionDefinition object containing the execution definition for the visualization
{{< /parameter >}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

chat_result = sdk.compute.ai_chat(workspace_id, "Display the revenue by product")
execution_definition = sdk.compute.build_exec_def_from_chat_result(chat_result)

print(execution_definition)
```
