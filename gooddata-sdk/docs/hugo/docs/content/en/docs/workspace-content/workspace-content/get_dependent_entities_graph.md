---
title: "get_dependent_entities_graph"
linkTitle: "get_dependent_entities_graph"
weight: 90
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``get_dependent_entities_graph(workspace_id: str)``

Returns *CatalogDependentEntitiesResponse*

There are dependencies among all catalog objects, the chain is the following:

`fact/attribute/label → dataset → metric → visualization → dashboard`

Some steps can be skipped, e.g. `fact → visualization`

We do not support `table → dataset` dependency yet.

## Example


```Python
# Get dependent entities Graph
sdk.catalog_workspace_content.get_dependent_entities_graph_from_entry_points(
    workspace_id="123"
)

#CatalogDependentEntitiesResponse(
#   graph=CatalogDependentEntitiesGraph(
#       nodes=[
#           CatalogDependentEntitiesNode(
#               id='campaign_channel_id',
#               type='attribute',
#               title='Campaign channel id'
#           ),
#           CatalogDependentEntitiesNode(
#               id='campaign_channels',
#               type='dataset',
#               title='Campaign channels'
#           )
#       ],
#       edges=[
#           [
#               CatalogEntityIdentifier(
#                   id='campaign_channel_id',
#                   type='attribute'
#               ),
#               CatalogEntityIdentifier(
#                   id='campaign_channels',
#                   type='dataset'
#               )
#           ]
#       ]
#   )
# )

```
