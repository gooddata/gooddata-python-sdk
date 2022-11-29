---
title: "get_dependent_entities_graph_from_entry_points"
linkTitle: "get_dependent_entities_graph_f..."
weight: 100
superheading: "catalog_workspace_content."
---

<!-- TODO -->

``get_dependent_entities_graph_from_entry_points(workspace_id: str, dependent_entities_request: CatalogDependentEntitiesRequest)``

Returns *CatalogDependentEntitiesResponse*

Extends [get_dependent_entities_graph](../get_dependent_entities_graph) with the entry point from which the graph is created.

## Example

```Python
# Get the identiffies
identifiers=[CatalogEntityIdentifier(id="campaign_channel_id", type="attribute")]
# Get dependent entities
dependent_entites_request = CatalogDependentEntitiesRequest(identifiers=identifiers)
# Get dependent entities Graph
sdk.catalog_workspace_content.get_dependent_entities_graph_from_entry_points(
    workspace_id="123",
    dependent_entities_request=dependent_entites_request
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
