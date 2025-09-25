# JsonApiAttributeOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAttributeHierarchyOutAttributes**](JsonApiAttributeHierarchyOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAttributeHierarchyOutRelationships**](JsonApiAttributeHierarchyOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_attribute_out_includes import JsonApiAttributeOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeOutIncludes from a JSON string
json_api_attribute_out_includes_instance = JsonApiAttributeOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeOutIncludes.to_json())

# convert the object into a dict
json_api_attribute_out_includes_dict = json_api_attribute_out_includes_instance.to_dict()
# create an instance of JsonApiAttributeOutIncludes from a dict
json_api_attribute_out_includes_from_dict = JsonApiAttributeOutIncludes.from_dict(json_api_attribute_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


