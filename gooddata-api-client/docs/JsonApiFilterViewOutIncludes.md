# JsonApiFilterViewOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserInAttributes**](JsonApiUserInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAnalyticalDashboardOutMeta**](JsonApiAnalyticalDashboardOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiUserInRelationships**](JsonApiUserInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_filter_view_out_includes import JsonApiFilterViewOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewOutIncludes from a JSON string
json_api_filter_view_out_includes_instance = JsonApiFilterViewOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewOutIncludes.to_json())

# convert the object into a dict
json_api_filter_view_out_includes_dict = json_api_filter_view_out_includes_instance.to_dict()
# create an instance of JsonApiFilterViewOutIncludes from a dict
json_api_filter_view_out_includes_from_dict = JsonApiFilterViewOutIncludes.from_dict(json_api_filter_view_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


