---
title: "get_full_catalog"
linkTitle: "get_full_catalog"
weight: 20
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``get_full_catalog(workspace_id: str)``

Returns *CatalogWorkspaceContent*.

Retrieve all datasets with attributes, facts, and metrics for a workspace.

## Example

```Python
# Get full catalog
workspace_content = sdk.catalog_workspace_content.get_full_catalog(workspace_id="123")

#CatalogWorkspaceContent(
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
#)
```
