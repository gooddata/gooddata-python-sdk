# JsonApiAttributeHierarchyPatch

JSON:API representation of patching attributeHierarchy entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAttributeHierarchyInAttributes**](JsonApiAttributeHierarchyInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_attribute_hierarchy_patch import JsonApiAttributeHierarchyPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeHierarchyPatch from a JSON string
json_api_attribute_hierarchy_patch_instance = JsonApiAttributeHierarchyPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeHierarchyPatch.to_json())

# convert the object into a dict
json_api_attribute_hierarchy_patch_dict = json_api_attribute_hierarchy_patch_instance.to_dict()
# create an instance of JsonApiAttributeHierarchyPatch from a dict
json_api_attribute_hierarchy_patch_from_dict = JsonApiAttributeHierarchyPatch.from_dict(json_api_attribute_hierarchy_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


