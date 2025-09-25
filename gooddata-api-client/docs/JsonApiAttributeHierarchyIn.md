# JsonApiAttributeHierarchyIn

JSON:API representation of attributeHierarchy entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAttributeHierarchyInAttributes**](JsonApiAttributeHierarchyInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_attribute_hierarchy_in import JsonApiAttributeHierarchyIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeHierarchyIn from a JSON string
json_api_attribute_hierarchy_in_instance = JsonApiAttributeHierarchyIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeHierarchyIn.to_json())

# convert the object into a dict
json_api_attribute_hierarchy_in_dict = json_api_attribute_hierarchy_in_instance.to_dict()
# create an instance of JsonApiAttributeHierarchyIn from a dict
json_api_attribute_hierarchy_in_from_dict = JsonApiAttributeHierarchyIn.from_dict(json_api_attribute_hierarchy_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


