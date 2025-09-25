# JsonApiDatasetOutRelationshipsWorkspaceDataFilters


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiWorkspaceDataFilterLinkage]**](JsonApiWorkspaceDataFilterLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_relationships_workspace_data_filters import JsonApiDatasetOutRelationshipsWorkspaceDataFilters

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutRelationshipsWorkspaceDataFilters from a JSON string
json_api_dataset_out_relationships_workspace_data_filters_instance = JsonApiDatasetOutRelationshipsWorkspaceDataFilters.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutRelationshipsWorkspaceDataFilters.to_json())

# convert the object into a dict
json_api_dataset_out_relationships_workspace_data_filters_dict = json_api_dataset_out_relationships_workspace_data_filters_instance.to_dict()
# create an instance of JsonApiDatasetOutRelationshipsWorkspaceDataFilters from a dict
json_api_dataset_out_relationships_workspace_data_filters_from_dict = JsonApiDatasetOutRelationshipsWorkspaceDataFilters.from_dict(json_api_dataset_out_relationships_workspace_data_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


