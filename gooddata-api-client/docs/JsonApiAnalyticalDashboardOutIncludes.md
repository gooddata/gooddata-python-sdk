# JsonApiAnalyticalDashboardOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDashboardPluginOutAttributes**](JsonApiDashboardPluginOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiDashboardPluginOutRelationships**](JsonApiDashboardPluginOutRelationships.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_includes import JsonApiAnalyticalDashboardOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutIncludes from a JSON string
json_api_analytical_dashboard_out_includes_instance = JsonApiAnalyticalDashboardOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutIncludes.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_includes_dict = json_api_analytical_dashboard_out_includes_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutIncludes from a dict
json_api_analytical_dashboard_out_includes_from_dict = JsonApiAnalyticalDashboardOutIncludes.from_dict(json_api_analytical_dashboard_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


