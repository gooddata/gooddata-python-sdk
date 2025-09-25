# JsonApiFilterContextPostOptionalId

JSON:API representation of filterContext entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardInAttributes**](JsonApiAnalyticalDashboardInAttributes.md) |  | 
**id** | **str** | API identifier of an object | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_filter_context_post_optional_id import JsonApiFilterContextPostOptionalId

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterContextPostOptionalId from a JSON string
json_api_filter_context_post_optional_id_instance = JsonApiFilterContextPostOptionalId.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterContextPostOptionalId.to_json())

# convert the object into a dict
json_api_filter_context_post_optional_id_dict = json_api_filter_context_post_optional_id_instance.to_dict()
# create an instance of JsonApiFilterContextPostOptionalId from a dict
json_api_filter_context_post_optional_id_from_dict = JsonApiFilterContextPostOptionalId.from_dict(json_api_filter_context_post_optional_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


