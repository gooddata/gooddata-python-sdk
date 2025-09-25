# JsonApiDashboardPluginPatch

JSON:API representation of patching dashboardPlugin entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDashboardPluginInAttributes**](JsonApiDashboardPluginInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_dashboard_plugin_patch import JsonApiDashboardPluginPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDashboardPluginPatch from a JSON string
json_api_dashboard_plugin_patch_instance = JsonApiDashboardPluginPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiDashboardPluginPatch.to_json())

# convert the object into a dict
json_api_dashboard_plugin_patch_dict = json_api_dashboard_plugin_patch_instance.to_dict()
# create an instance of JsonApiDashboardPluginPatch from a dict
json_api_dashboard_plugin_patch_from_dict = JsonApiDashboardPluginPatch.from_dict(json_api_dashboard_plugin_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


