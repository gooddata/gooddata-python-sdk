# DeclarativeWorkspace

A declarative form of a particular workspace.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**automations** | [**List[DeclarativeAutomation]**](DeclarativeAutomation.md) |  | [optional] 
**cache_extra_limit** | **int** | Extra cache limit allocated to specific workspace. In case there is extra cache budget setup for organization, it can be split between multiple workspaces. | [optional] 
**custom_application_settings** | [**List[DeclarativeCustomApplicationSetting]**](DeclarativeCustomApplicationSetting.md) | A list of workspace custom settings. | [optional] 
**data_source** | [**WorkspaceDataSource**](WorkspaceDataSource.md) |  | [optional] 
**description** | **str** | Description of the workspace | [optional] 
**early_access** | **str** | Early access defined on level Workspace | [optional] 
**early_access_values** | **List[str]** | Early access defined on level Workspace | [optional] 
**filter_views** | [**List[DeclarativeFilterView]**](DeclarativeFilterView.md) |  | [optional] 
**hierarchy_permissions** | [**List[DeclarativeWorkspaceHierarchyPermission]**](DeclarativeWorkspaceHierarchyPermission.md) |  | [optional] 
**id** | **str** | Identifier of a workspace | 
**model** | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md) |  | [optional] 
**name** | **str** | Name of a workspace to view. | 
**parent** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | [optional] 
**permissions** | [**List[DeclarativeSingleWorkspacePermission]**](DeclarativeSingleWorkspacePermission.md) |  | [optional] 
**prefix** | **str** | Custom prefix of entity identifiers in workspace | [optional] 
**settings** | [**List[DeclarativeSetting]**](DeclarativeSetting.md) | A list of workspace settings. | [optional] 
**user_data_filters** | [**List[DeclarativeUserDataFilter]**](DeclarativeUserDataFilter.md) | A list of workspace user data filters. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_workspace import DeclarativeWorkspace

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeWorkspace from a JSON string
declarative_workspace_instance = DeclarativeWorkspace.from_json(json)
# print the JSON string representation of the object
print(DeclarativeWorkspace.to_json())

# convert the object into a dict
declarative_workspace_dict = declarative_workspace_instance.to_dict()
# create an instance of DeclarativeWorkspace from a dict
declarative_workspace_from_dict = DeclarativeWorkspace.from_dict(declarative_workspace_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


