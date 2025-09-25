# JsonApiAnalyticalDashboardOutRelationshipsDatasets


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiDatasetLinkage]**](JsonApiDatasetLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_relationships_datasets import JsonApiAnalyticalDashboardOutRelationshipsDatasets

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsDatasets from a JSON string
json_api_analytical_dashboard_out_relationships_datasets_instance = JsonApiAnalyticalDashboardOutRelationshipsDatasets.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutRelationshipsDatasets.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_relationships_datasets_dict = json_api_analytical_dashboard_out_relationships_datasets_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutRelationshipsDatasets from a dict
json_api_analytical_dashboard_out_relationships_datasets_from_dict = JsonApiAnalyticalDashboardOutRelationshipsDatasets.from_dict(json_api_analytical_dashboard_out_relationships_datasets_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


