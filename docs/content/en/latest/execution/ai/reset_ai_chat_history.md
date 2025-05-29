---
title: "reset_ai_chat_history"
linkTitle: "reset_ai_chat_history"
weight: 97
superheading: "compute."
---

``reset_ai_chat_history(workspace_id: str) -> None``

Reset AI chat history in GoodData workspace.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="str" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="true"%}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

sdk.compute.reset_ai_chat_history(workspace_id)
```
