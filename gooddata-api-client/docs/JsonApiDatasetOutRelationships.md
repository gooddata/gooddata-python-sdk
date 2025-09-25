# JsonApiDatasetOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregated_facts** | [**JsonApiDatasetOutRelationshipsAggregatedFacts**](JsonApiDatasetOutRelationshipsAggregatedFacts.md) |  | [optional] 
**attributes** | [**JsonApiAttributeHierarchyOutRelationshipsAttributes**](JsonApiAttributeHierarchyOutRelationshipsAttributes.md) |  | [optional] 
**facts** | [**JsonApiDatasetOutRelationshipsFacts**](JsonApiDatasetOutRelationshipsFacts.md) |  | [optional] 
**references** | [**JsonApiAnalyticalDashboardOutRelationshipsDatasets**](JsonApiAnalyticalDashboardOutRelationshipsDatasets.md) |  | [optional] 
**workspace_data_filters** | [**JsonApiDatasetOutRelationshipsWorkspaceDataFilters**](JsonApiDatasetOutRelationshipsWorkspaceDataFilters.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_relationships import JsonApiDatasetOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutRelationships from a JSON string
json_api_dataset_out_relationships_instance = JsonApiDatasetOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutRelationships.to_json())

# convert the object into a dict
json_api_dataset_out_relationships_dict = json_api_dataset_out_relationships_instance.to_dict()
# create an instance of JsonApiDatasetOutRelationships from a dict
json_api_dataset_out_relationships_from_dict = JsonApiDatasetOutRelationships.from_dict(json_api_dataset_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


