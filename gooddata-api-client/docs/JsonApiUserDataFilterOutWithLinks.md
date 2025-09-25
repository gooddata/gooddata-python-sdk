# JsonApiUserDataFilterOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserDataFilterInAttributes**](JsonApiUserDataFilterInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiUserDataFilterOutRelationships**](JsonApiUserDataFilterOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_out_with_links import JsonApiUserDataFilterOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterOutWithLinks from a JSON string
json_api_user_data_filter_out_with_links_instance = JsonApiUserDataFilterOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterOutWithLinks.to_json())

# convert the object into a dict
json_api_user_data_filter_out_with_links_dict = json_api_user_data_filter_out_with_links_instance.to_dict()
# create an instance of JsonApiUserDataFilterOutWithLinks from a dict
json_api_user_data_filter_out_with_links_from_dict = JsonApiUserDataFilterOutWithLinks.from_dict(json_api_user_data_filter_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


