---
title: "ai_chat"
linkTitle: "ai_chat"
weight: 96
superheading: "compute."
---

``ai_chat(workspace_id: str, question: str) -> ChatResult``

Chat with AI in GoodData workspace.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="str" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{< parameter p_name="question" p_type="str" >}}
The question to ask the AI.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_name="chat_result" p_type="ChatResult" >}}
Chat response
{{< /parameter >}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

chat_result = sdk.compute.ai_chat(workspace_id, "Display the revenue by product")

print(chat_result)
```
