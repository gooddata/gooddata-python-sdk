# DependentEntitiesNode


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**title** | **str** |  | [optional] 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.dependent_entities_node import DependentEntitiesNode

# TODO update the JSON string below
json = "{}"
# create an instance of DependentEntitiesNode from a JSON string
dependent_entities_node_instance = DependentEntitiesNode.from_json(json)
# print the JSON string representation of the object
print(DependentEntitiesNode.to_json())

# convert the object into a dict
dependent_entities_node_dict = dependent_entities_node_instance.to_dict()
# create an instance of DependentEntitiesNode from a dict
dependent_entities_node_from_dict = DependentEntitiesNode.from_dict(dependent_entities_node_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


