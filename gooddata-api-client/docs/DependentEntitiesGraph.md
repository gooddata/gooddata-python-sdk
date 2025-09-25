# DependentEntitiesGraph


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**edges** | **List[List[EntityIdentifier]]** |  | 
**nodes** | [**List[DependentEntitiesNode]**](DependentEntitiesNode.md) |  | 

## Example

```python
from gooddata_api_client.models.dependent_entities_graph import DependentEntitiesGraph

# TODO update the JSON string below
json = "{}"
# create an instance of DependentEntitiesGraph from a JSON string
dependent_entities_graph_instance = DependentEntitiesGraph.from_json(json)
# print the JSON string representation of the object
print(DependentEntitiesGraph.to_json())

# convert the object into a dict
dependent_entities_graph_dict = dependent_entities_graph_instance.to_dict()
# create an instance of DependentEntitiesGraph from a dict
dependent_entities_graph_from_dict = DependentEntitiesGraph.from_dict(dependent_entities_graph_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


