# JsonApiFilterContextOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardInAttributes**](JsonApiAnalyticalDashboardInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiFilterContextOutRelationships**](JsonApiFilterContextOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_filter_context_out_with_links import JsonApiFilterContextOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterContextOutWithLinks from a JSON string
json_api_filter_context_out_with_links_instance = JsonApiFilterContextOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterContextOutWithLinks.to_json())

# convert the object into a dict
json_api_filter_context_out_with_links_dict = json_api_filter_context_out_with_links_instance.to_dict()
# create an instance of JsonApiFilterContextOutWithLinks from a dict
json_api_filter_context_out_with_links_from_dict = JsonApiFilterContextOutWithLinks.from_dict(json_api_filter_context_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


