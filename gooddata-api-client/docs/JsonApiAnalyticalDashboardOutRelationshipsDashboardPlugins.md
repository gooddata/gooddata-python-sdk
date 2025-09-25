# JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiDashboardPluginLinkage]**](JsonApiDashboardPluginLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_relationships_dashboard_plugins import JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins from a JSON string
json_api_analytical_dashboard_out_relationships_dashboard_plugins_instance = JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_relationships_dashboard_plugins_dict = json_api_analytical_dashboard_out_relationships_dashboard_plugins_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins from a dict
json_api_analytical_dashboard_out_relationships_dashboard_plugins_from_dict = JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins.from_dict(json_api_analytical_dashboard_out_relationships_dashboard_plugins_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


