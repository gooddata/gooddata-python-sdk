---
title: "get_labels_catalog"
linkTitle: "get_labels_catalog"
weight: 60
superheading: "catalog_workspace_content."
---



``get_labels_catalog(workspace_id: str)``

Gets all labels in a given workspace.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="list[CatalogLabel]" >}}
List of all labels in a given workspace.
{{< /parameter >}}
{{% /parameters-block %}}

## Example

```python
# Get all labels
labels = sdk.catalog_workspace_content.get_labels_catalog(workspace_id="123")
# [
#   CatalogLabel(
#       id=campaign_channel_id,
#       title=Campaign channel id
#   ),
#   CatalogLabel(
#       id=campaign_channels.category,
#       title=Category
#   ),
#   CatalogLabel(
#       id=type,
#       title=Type
#   ),
#   ...
# ]
```
