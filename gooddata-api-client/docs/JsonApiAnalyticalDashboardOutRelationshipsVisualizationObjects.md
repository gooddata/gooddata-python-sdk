# JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiVisualizationObjectLinkage]**](JsonApiVisualizationObjectLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_relationships_visualization_objects import JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects from a JSON string
json_api_analytical_dashboard_out_relationships_visualization_objects_instance = JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_relationships_visualization_objects_dict = json_api_analytical_dashboard_out_relationships_visualization_objects_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects from a dict
json_api_analytical_dashboard_out_relationships_visualization_objects_from_dict = JsonApiAnalyticalDashboardOutRelationshipsVisualizationObjects.from_dict(json_api_analytical_dashboard_out_relationships_visualization_objects_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


