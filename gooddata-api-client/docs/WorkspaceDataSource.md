# WorkspaceDataSource

The data source used for the particular workspace instead of the one defined in the LDM inherited from its parent workspace. Such data source cannot be defined for a single or a top-parent workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the used data source. | 
**schema_path** | **List[str]** | The full schema path as array of its path parts. Will be rendered as subPath1.subPath2... | [optional] 

## Example

```python
from gooddata_api_client.models.workspace_data_source import WorkspaceDataSource

# TODO update the JSON string below
json = "{}"
# create an instance of WorkspaceDataSource from a JSON string
workspace_data_source_instance = WorkspaceDataSource.from_json(json)
# print the JSON string representation of the object
print(WorkspaceDataSource.to_json())

# convert the object into a dict
workspace_data_source_dict = workspace_data_source_instance.to_dict()
# create an instance of WorkspaceDataSource from a dict
workspace_data_source_from_dict = WorkspaceDataSource.from_dict(workspace_data_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


