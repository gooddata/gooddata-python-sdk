---
title: "get_attributes_catalog"
linkTitle: "get_attributes_catalog"
weight: 50
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.get_attributes_catalog" >}}

## Example

```python
# Get attributes
attributes = sdk.catalog_workspace_content.get_attributes_catalog(workspace_id="123")

# [
#   CatalogAttribute(
#       id=campaign_channel_id,
#       title=Campaign channel id,
#       labels=[]
#   ),
#   CatalogAttribute(
#       id=campaign_channels.category,
#       title=Category,
#       labels=[]
#   ),
#   CatalogAttribute(
#       id=type,
#       title=Type,
#       labels=[]
#   ),
# ...
# ]

```
