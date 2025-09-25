# JsonApiAnalyticalDashboardOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboards** | [**JsonApiAnalyticalDashboardOutRelationshipsAnalyticalDashboards**](JsonApiAnalyticalDashboardOutRelationshipsAnalyticalDashboards.md) |  | [optional] 
**created_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 
**dashboard_plugins** | [**JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins**](JsonApiAnalyticalDashboardOutRelationshipsDashboardPlugins.md) |  | [optional] 
**datasets** | [**JsonApiAnalyticalDashboardOutRelationshipsDatasets**](JsonApiAnalyticalDashboardOutRelationshipsDatasets.md) |  | [optional] 
**filter_contexts** | [**JsonApiAnalyticalDashboardOutRelationshipsFilterContexts**](JsonApiAnalyticalDashboardOutRelationshipsFilterContexts.md) |  | [optional] 
**labels** | [**JsonApiAnalyticalDashboardOutRelationshipsLabels**](JsonApiAnalyticalDashboardOutRelationshipsLabels.md) |  | [optional] 
**metrics** | [**JsonApiAnalyticalDashboardOutRelationshipsMetrics**](JsonApiAnalyticalDashboardOutRelationshipsMetrics.md) |  | [optional] 
**modified_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 
**visualization_objects** | [**JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects**](JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_relationships import JsonApiAnalyticalDashboardOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutRelationships from a JSON string
json_api_analytical_dashboard_out_relationships_instance = JsonApiAnalyticalDashboardOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutRelationships.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_relationships_dict = json_api_analytical_dashboard_out_relationships_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutRelationships from a dict
json_api_analytical_dashboard_out_relationships_from_dict = JsonApiAnalyticalDashboardOutRelationships.from_dict(json_api_analytical_dashboard_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


