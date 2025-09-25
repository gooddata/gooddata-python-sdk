# JsonApiDashboardPluginOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiDashboardPluginOutWithLinks]**](JsonApiDashboardPluginOutWithLinks.md) |  | 
**included** | [**List[JsonApiUserIdentifierOutWithLinks]**](JsonApiUserIdentifierOutWithLinks.md) | Included resources | [optional] 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_dashboard_plugin_out_list import JsonApiDashboardPluginOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDashboardPluginOutList from a JSON string
json_api_dashboard_plugin_out_list_instance = JsonApiDashboardPluginOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiDashboardPluginOutList.to_json())

# convert the object into a dict
json_api_dashboard_plugin_out_list_dict = json_api_dashboard_plugin_out_list_instance.to_dict()
# create an instance of JsonApiDashboardPluginOutList from a dict
json_api_dashboard_plugin_out_list_from_dict = JsonApiDashboardPluginOutList.from_dict(json_api_dashboard_plugin_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


