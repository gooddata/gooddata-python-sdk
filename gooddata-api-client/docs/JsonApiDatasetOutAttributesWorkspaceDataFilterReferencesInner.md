# JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner

Workspace data filter reference.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filter_column** | **str** |  | 
**filter_column_data_type** | **str** |  | 
**filter_id** | [**DatasetWorkspaceDataFilterIdentifier**](DatasetWorkspaceDataFilterIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_attributes_workspace_data_filter_references_inner import JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner from a JSON string
json_api_dataset_out_attributes_workspace_data_filter_references_inner_instance = JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner.to_json())

# convert the object into a dict
json_api_dataset_out_attributes_workspace_data_filter_references_inner_dict = json_api_dataset_out_attributes_workspace_data_filter_references_inner_instance.to_dict()
# create an instance of JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner from a dict
json_api_dataset_out_attributes_workspace_data_filter_references_inner_from_dict = JsonApiDatasetOutAttributesWorkspaceDataFilterReferencesInner.from_dict(json_api_dataset_out_attributes_workspace_data_filter_references_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


