# JsonApiDashboardPluginPostOptionalId

JSON:API representation of dashboardPlugin entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDashboardPluginInAttributes**](JsonApiDashboardPluginInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_dashboard_plugin_post_optional_id import JsonApiDashboardPluginPostOptionalId

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDashboardPluginPostOptionalId from a JSON string
json_api_dashboard_plugin_post_optional_id_instance = JsonApiDashboardPluginPostOptionalId.from_json(json)
# print the JSON string representation of the object
print(JsonApiDashboardPluginPostOptionalId.to_json())

# convert the object into a dict
json_api_dashboard_plugin_post_optional_id_dict = json_api_dashboard_plugin_post_optional_id_instance.to_dict()
# create an instance of JsonApiDashboardPluginPostOptionalId from a dict
json_api_dashboard_plugin_post_optional_id_from_dict = JsonApiDashboardPluginPostOptionalId.from_dict(json_api_dashboard_plugin_post_optional_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


