---
title: "set_metadata_localization"
linkTitle: "set_metadata_localization"
weight: 53
superheading: "catalog_workspace."
---

``set_metadata_localization(workspace_id: str, encoded_xml: bytes) -> None``

Set the metadata localization for a workspace.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the workspace to which the metadata localization applies.
{{< /parameter >}}
{{< parameter p_name="encoded_xml" p_type="bytes" >}}
The encoded XML metadata to be set.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" None="yes" %}}
{{% /parameters-block %}}

## Example

```python
# Set the metadata localization for a workspace using encoded XML.
sdk.catalog_workspace.set_metadata_localization(
    workspace_id="123",
    encoded_xml=b"<xml>...</xml>"
)
