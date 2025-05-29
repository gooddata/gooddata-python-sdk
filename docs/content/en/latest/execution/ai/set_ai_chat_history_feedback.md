---
title: "set_ai_chat_history_feedback"
linkTitle: "set_ai_chat_history_feedback"
weight: 101
superheading: "compute."
---
``set_ai_chat_history_feedback(workspace_id: str, interaction_id: str, user_feedback: str, chat_history_interaction_id: str, thread_id_suffix: str = "") -> None``

Set feedback for an AI chat history interaction.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="str" >}}
workspace identifier
{{< /parameter >}}
{{< parameter p_name="interaction_id" p_type="str" >}}
feedback to provide ("POSITIVE", "NEGATIVE" or "NONE").
{{< /parameter >}}
{{< parameter p_name="user_feedback" p_type="str" >}}
interaction id to provide feedback for.
{{< /parameter >}}
{{< parameter p_name="chat_history_interaction_id" p_type="str" >}}
suffix to identify a specific chat thread. Defaults to "".
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="true"%}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

sdk.compute.set_ai_chat_history_feedback(workspace_id, "POSITIVE", "123", "456")
```
