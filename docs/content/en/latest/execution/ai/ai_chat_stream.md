---
title: "ai_chat_stream"
linkTitle: "ai_chat_stream"
weight: 93
superheading: "compute."
---

``ai_chat_stream(workspace_id: str, question: str) -> Iterator[Any]``

Chat with AI in GoodData workspace. Stream the response.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="str" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{< parameter p_name="question" p_type="str" >}}
The question to ask the AI.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_name="chat_result" p_type="Iterator[Any]" >}}
Yields parsed JSON objects from each SSE event's data field{{< /parameter >}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

chat_result = sdk.compute.ai_chat_stream(workspace_id, "Display the revenue by product")
```
