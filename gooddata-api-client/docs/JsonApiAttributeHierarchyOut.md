# JsonApiAttributeHierarchyOut

JSON:API representation of attributeHierarchy entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAttributeHierarchyOutAttributes**](JsonApiAttributeHierarchyOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAttributeHierarchyOutRelationships**](JsonApiAttributeHierarchyOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_attribute_hierarchy_out import JsonApiAttributeHierarchyOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeHierarchyOut from a JSON string
json_api_attribute_hierarchy_out_instance = JsonApiAttributeHierarchyOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeHierarchyOut.to_json())

# convert the object into a dict
json_api_attribute_hierarchy_out_dict = json_api_attribute_hierarchy_out_instance.to_dict()
# create an instance of JsonApiAttributeHierarchyOut from a dict
json_api_attribute_hierarchy_out_from_dict = JsonApiAttributeHierarchyOut.from_dict(json_api_attribute_hierarchy_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


