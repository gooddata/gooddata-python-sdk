# JsonApiAttributeHierarchyOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiAttributeHierarchyOutWithLinks]**](JsonApiAttributeHierarchyOutWithLinks.md) |  | 
**included** | [**List[JsonApiAttributeHierarchyOutIncludes]**](JsonApiAttributeHierarchyOutIncludes.md) | Included resources | [optional] 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_attribute_hierarchy_out_list import JsonApiAttributeHierarchyOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeHierarchyOutList from a JSON string
json_api_attribute_hierarchy_out_list_instance = JsonApiAttributeHierarchyOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeHierarchyOutList.to_json())

# convert the object into a dict
json_api_attribute_hierarchy_out_list_dict = json_api_attribute_hierarchy_out_list_instance.to_dict()
# create an instance of JsonApiAttributeHierarchyOutList from a dict
json_api_attribute_hierarchy_out_list_from_dict = JsonApiAttributeHierarchyOutList.from_dict(json_api_attribute_hierarchy_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


