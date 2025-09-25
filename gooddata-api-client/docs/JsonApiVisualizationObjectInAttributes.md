# JsonApiVisualizationObjectInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | **object** | Free-form JSON content. Maximum supported length is 250000 characters. | 
**description** | **str** |  | [optional] 
**is_hidden** | **bool** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_visualization_object_in_attributes import JsonApiVisualizationObjectInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiVisualizationObjectInAttributes from a JSON string
json_api_visualization_object_in_attributes_instance = JsonApiVisualizationObjectInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiVisualizationObjectInAttributes.to_json())

# convert the object into a dict
json_api_visualization_object_in_attributes_dict = json_api_visualization_object_in_attributes_instance.to_dict()
# create an instance of JsonApiVisualizationObjectInAttributes from a dict
json_api_visualization_object_in_attributes_from_dict = JsonApiVisualizationObjectInAttributes.from_dict(json_api_visualization_object_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


