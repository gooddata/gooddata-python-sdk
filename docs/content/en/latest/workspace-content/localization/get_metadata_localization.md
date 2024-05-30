---
title: "get_metadata_localization"
linkTitle: "get_metadata_localization"
weight: 52
superheading: "catalog_workspace."
---

``get_metadata_localization(workspace_id: str, target_language: str) -> bytes``

Retrieve the metadata localization for a workspace.

{{% parameters-block title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
The ID of the workspace for which to retrieve the metadata localization.
{{< /parameter >}}
{{< parameter p_name="target_language" p_type="string" >}}
The target language code for the localization.
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns" %}}
{{< parameter p_type="bytes" >}}
Object Containing declarative Analytical Model.
{{< /parameter >}}The encoded metadata localization in the target language.
{{% /parameters-block %}}

## Example

```python
# Retrieve metadata localization for a workspace in the specified language.
localization = sdk.catalog_workspace.get_metadata_localization(
    workspace_id="123",
    target_language="de-DE"
)
