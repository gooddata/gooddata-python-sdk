---
title: "get_full_catalog"
linkTitle: "get_full_catalog"
weight: 20
superheading: "catalog_workspace_content."
---

{{< api-ref "sdk.CatalogWorkspaceContentService.get_full_catalog" >}}

## Example

```python
# Get full catalog
workspace_content = sdk.catalog_workspace_content.get_full_catalog(workspace_id="123")

# CatalogWorkspaceContent(
#   datasets=[
#       CatalogDataset(
#           id=campaign_channels,
#           title=Campaign channels,
#           facts=[
#               CatalogFact(
#                   id=spend,
#                   title=Spend
#               ),
#           CatalogFact(
#               id=budget,
#               title=Budget
#           )
#   ],
#   ...
# )
```
