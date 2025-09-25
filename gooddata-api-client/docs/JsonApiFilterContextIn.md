# JsonApiFilterContextIn

JSON:API representation of filterContext entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAnalyticalDashboardInAttributes**](JsonApiAnalyticalDashboardInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_filter_context_in import JsonApiFilterContextIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterContextIn from a JSON string
json_api_filter_context_in_instance = JsonApiFilterContextIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterContextIn.to_json())

# convert the object into a dict
json_api_filter_context_in_dict = json_api_filter_context_in_instance.to_dict()
# create an instance of JsonApiFilterContextIn from a dict
json_api_filter_context_in_from_dict = JsonApiFilterContextIn.from_dict(json_api_filter_context_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


