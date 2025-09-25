# DeclarativeVisualizationObject


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | 
**created_at** | **str** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** | Visualization object description. | [optional] 
**id** | **str** | Visualization object ID. | 
**is_hidden** | **bool** | If true, this visualization object is hidden from AI search results. | [optional] 
**modified_at** | **str** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Visualization object title. | 

## Example

```python
from gooddata_api_client.models.declarative_visualization_object import DeclarativeVisualizationObject

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeVisualizationObject from a JSON string
declarative_visualization_object_instance = DeclarativeVisualizationObject.from_json(json)
# print the JSON string representation of the object
print(DeclarativeVisualizationObject.to_json())

# convert the object into a dict
declarative_visualization_object_dict = declarative_visualization_object_instance.to_dict()
# create an instance of DeclarativeVisualizationObject from a dict
declarative_visualization_object_from_dict = DeclarativeVisualizationObject.from_dict(declarative_visualization_object_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


