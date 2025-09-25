# JsonApiAttributeHierarchyOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**content** | **object** | Free-form JSON content. Maximum supported length is 15000 characters. | [optional] 
**created_at** | **datetime** |  | [optional] 
**description** | **str** |  | [optional] 
**modified_at** | **datetime** |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_attribute_hierarchy_out_attributes import JsonApiAttributeHierarchyOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeHierarchyOutAttributes from a JSON string
json_api_attribute_hierarchy_out_attributes_instance = JsonApiAttributeHierarchyOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeHierarchyOutAttributes.to_json())

# convert the object into a dict
json_api_attribute_hierarchy_out_attributes_dict = json_api_attribute_hierarchy_out_attributes_instance.to_dict()
# create an instance of JsonApiAttributeHierarchyOutAttributes from a dict
json_api_attribute_hierarchy_out_attributes_from_dict = JsonApiAttributeHierarchyOutAttributes.from_dict(json_api_attribute_hierarchy_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


