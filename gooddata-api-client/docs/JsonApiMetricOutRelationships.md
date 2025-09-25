# JsonApiMetricOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAttributeHierarchyOutRelationshipsAttributes**](JsonApiAttributeHierarchyOutRelationshipsAttributes.md) |  | [optional] 
**created_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 
**datasets** | [**JsonApiAnalyticalDashboardOutRelationshipsDatasets**](JsonApiAnalyticalDashboardOutRelationshipsDatasets.md) |  | [optional] 
**facts** | [**JsonApiDatasetOutRelationshipsFacts**](JsonApiDatasetOutRelationshipsFacts.md) |  | [optional] 
**labels** | [**JsonApiAnalyticalDashboardOutRelationshipsLabels**](JsonApiAnalyticalDashboardOutRelationshipsLabels.md) |  | [optional] 
**metrics** | [**JsonApiAnalyticalDashboardOutRelationshipsMetrics**](JsonApiAnalyticalDashboardOutRelationshipsMetrics.md) |  | [optional] 
**modified_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_metric_out_relationships import JsonApiMetricOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiMetricOutRelationships from a JSON string
json_api_metric_out_relationships_instance = JsonApiMetricOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiMetricOutRelationships.to_json())

# convert the object into a dict
json_api_metric_out_relationships_dict = json_api_metric_out_relationships_instance.to_dict()
# create an instance of JsonApiMetricOutRelationships from a dict
json_api_metric_out_relationships_from_dict = JsonApiMetricOutRelationships.from_dict(json_api_metric_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


