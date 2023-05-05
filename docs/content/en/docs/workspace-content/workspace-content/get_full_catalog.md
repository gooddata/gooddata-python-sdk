---
title: "get_full_catalog"
linkTitle: "get_full_catalog"
weight: 20
superheading: "catalog_workspace_content."
---



``get_full_catalog(workspace_id: str)``

Gets catalog for a workspace. Catalog contains all data sets and metrics defined in that workspace.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="CatalogWorkspaceContent" >}}
Object containing all data sets and metrics.
{{< /parameter >}}
{{% /parameters-block %}}

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
