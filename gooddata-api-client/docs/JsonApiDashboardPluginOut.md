# JsonApiDashboardPluginOut

JSON:API representation of dashboardPlugin entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDashboardPluginOutAttributes**](JsonApiDashboardPluginOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiDashboardPluginOutRelationships**](JsonApiDashboardPluginOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_dashboard_plugin_out import JsonApiDashboardPluginOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDashboardPluginOut from a JSON string
json_api_dashboard_plugin_out_instance = JsonApiDashboardPluginOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiDashboardPluginOut.to_json())

# convert the object into a dict
json_api_dashboard_plugin_out_dict = json_api_dashboard_plugin_out_instance.to_dict()
# create an instance of JsonApiDashboardPluginOut from a dict
json_api_dashboard_plugin_out_from_dict = JsonApiDashboardPluginOut.from_dict(json_api_dashboard_plugin_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


