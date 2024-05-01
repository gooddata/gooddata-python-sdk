---
title: "get_attributes_catalog"
linkTitle: "get_attributes_catalog"
weight: 50
superheading: "catalog_workspace_content."
---



``get_attributes_catalog(workspace_id: str)``

Gets all attributes in a given workspace.

{{% parameters-block  title="Parameters" %}}
{{< parameter p_name="workspace_id" p_type="string" >}}
Workspace identification string e.g. "demo"
{{< /parameter >}}
{{% /parameters-block %}}

{{% parameters-block title="Returns"%}}
{{< parameter p_type="list[CatalogAttribute]" >}}
List of all attributes in a given workspace.
{{< /parameter >}}
{{% /parameters-block %}}

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
