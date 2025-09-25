# DeclarativeWorkspaceDataFilter

Workspace Data Filters serving the filtering of what data users can see in workspaces.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_name** | **str** | Workspace Data Filters column name. Data are filtered using this physical column. | 
**description** | **str** | Workspace Data Filters description. | [optional] 
**id** | **str** | Workspace Data Filters ID. This ID is further used to refer to this instance. | 
**title** | **str** | Workspace Data Filters title. | 
**workspace** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | 
**workspace_data_filter_settings** | [**List[DeclarativeWorkspaceDataFilterSetting]**](DeclarativeWorkspaceDataFilterSetting.md) | Filter settings specifying values of filters valid for the workspace. | 

## Example

```python
from gooddata_api_client.models.declarative_workspace_data_filter import DeclarativeWorkspaceDataFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspaceDataFilter from a JSON string
declarative_workspace_data_filter_instance = DeclarativeWorkspaceDataFilter.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspaceDataFilter.to_json())

# convert the object into a dict
declarative_workspace_data_filter_dict = declarative_workspace_data_filter_instance.to_dict()
# create an instance of DeclarativeWorkspaceDataFilter from a dict
declarative_workspace_data_filter_from_dict = DeclarativeWorkspaceDataFilter.from_dict(declarative_workspace_data_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


