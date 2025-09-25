# DatasetWorkspaceDataFilterIdentifier

Identifier of a workspace data filter.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Workspace Data Filters ID. | 
**type** | **str** | Filter type. | 

## Example

```python
from gooddata_api_client.models.dataset_workspace_data_filter_identifier import DatasetWorkspaceDataFilterIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetWorkspaceDataFilterIdentifier from a JSON string
dataset_workspace_data_filter_identifier_instance = DatasetWorkspaceDataFilterIdentifier.from_json(json)
# print the JSON string representation of the object
print(DatasetWorkspaceDataFilterIdentifier.to_json())

# convert the object into a dict
dataset_workspace_data_filter_identifier_dict = dataset_workspace_data_filter_identifier_instance.to_dict()
# create an instance of DatasetWorkspaceDataFilterIdentifier from a dict
dataset_workspace_data_filter_identifier_from_dict = DatasetWorkspaceDataFilterIdentifier.from_dict(dataset_workspace_data_filter_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


