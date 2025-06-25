---
title: "get_labels_catalog"
linkTitle: "get_labels_catalog"
weight: 60
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.get_labels_catalog" >}}

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
