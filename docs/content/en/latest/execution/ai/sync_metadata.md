---
title: "sync_metadata"
linkTitle: "sync_metadata"
weight: 100
superheading: "compute."
---

``sync_metadata(workspace_id: str, async_req: bool = False) -> None``

Sync metadata in GoodData workspace.


{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="str" >}}
The ID of the GoodData Workspace.
{{< /parameter >}}
{{< parameter p_name="async_req" p_type="bool" >}}
Whether to perform the request asynchronously.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="true"%}}
{{% /parameters-block %}}


## Example

```python

host = "https://www.example.com"
token = "<your_personal_access_token>"
sdk = GoodDataSdk.create(host, token)

sdk.compute.sync_metadata(workspace_id)
```
