# JsonApiAttributeOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiAttributeOutWithLinks]**](JsonApiAttributeOutWithLinks.md) |  | 
**included** | [**List[JsonApiAttributeOutIncludes]**](JsonApiAttributeOutIncludes.md) | Included resources | [optional] 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_attribute_out_list import JsonApiAttributeOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAttributeOutList from a JSON string
json_api_attribute_out_list_instance = JsonApiAttributeOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiAttributeOutList.to_json())

# convert the object into a dict
json_api_attribute_out_list_dict = json_api_attribute_out_list_instance.to_dict()
# create an instance of JsonApiAttributeOutList from a dict
json_api_attribute_out_list_from_dict = JsonApiAttributeOutList.from_dict(json_api_attribute_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


