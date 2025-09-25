# JsonApiWorkspaceInAttributesDataSource

The data source used for the particular workspace instead of the one defined in the LDM inherited from its parent workspace. Such data source cannot be defined for a single or a top-parent workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The ID of the used data source. | 
**schema_path** | **List[str]** | The full schema path as array of its path parts. Will be rendered as subPath1.subPath2... | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_workspace_in_attributes_data_source import JsonApiWorkspaceInAttributesDataSource

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiWorkspaceInAttributesDataSource from a JSON string
json_api_workspace_in_attributes_data_source_instance = JsonApiWorkspaceInAttributesDataSource.from_json(json)
# print the JSON string representation of the object
print(JsonApiWorkspaceInAttributesDataSource.to_json())

# convert the object into a dict
json_api_workspace_in_attributes_data_source_dict = json_api_workspace_in_attributes_data_source_instance.to_dict()
# create an instance of JsonApiWorkspaceInAttributesDataSource from a dict
json_api_workspace_in_attributes_data_source_from_dict = JsonApiWorkspaceInAttributesDataSource.from_dict(json_api_workspace_in_attributes_data_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


