# JsonApiDashboardPluginIn

JSON:API representation of dashboardPlugin entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDashboardPluginInAttributes**](JsonApiDashboardPluginInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_dashboard_plugin_in import JsonApiDashboardPluginIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDashboardPluginIn from a JSON string
json_api_dashboard_plugin_in_instance = JsonApiDashboardPluginIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiDashboardPluginIn.to_json())

# convert the object into a dict
json_api_dashboard_plugin_in_dict = json_api_dashboard_plugin_in_instance.to_dict()
# create an instance of JsonApiDashboardPluginIn from a dict
json_api_dashboard_plugin_in_from_dict = JsonApiDashboardPluginIn.from_dict(json_api_dashboard_plugin_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


