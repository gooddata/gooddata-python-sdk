# DeclarativeWorkspace

A declarative form of a particular workspace.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of a workspace | 
**name** | **str** | Name of a workspace to view. | 
**automations** | [**[DeclarativeAutomation]**](DeclarativeAutomation.md) |  | [optional] 
**cache_extra_limit** | **int** | Extra cache limit allocated to specific workspace. In case there is extra cache budget setup for organization, it can be split between multiple workspaces. | [optional] 
**custom_application_settings** | [**[DeclarativeCustomApplicationSetting]**](DeclarativeCustomApplicationSetting.md) | A list of workspace custom settings. | [optional] 
**data_source** | [**WorkspaceDataSource**](WorkspaceDataSource.md) |  | [optional] 
**description** | **str** | Description of the workspace | [optional] 
**early_access** | **str** | Early access defined on level Workspace | [optional] 
**early_access_values** | **[str]** | Early access defined on level Workspace | [optional] 
**filter_views** | [**[DeclarativeFilterView]**](DeclarativeFilterView.md) |  | [optional] 
**hierarchy_permissions** | [**[DeclarativeWorkspaceHierarchyPermission]**](DeclarativeWorkspaceHierarchyPermission.md) |  | [optional] 
**model** | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md) |  | [optional] 
**parent** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | [optional] 
**permissions** | [**[DeclarativeSingleWorkspacePermission]**](DeclarativeSingleWorkspacePermission.md) |  | [optional] 
**prefix** | **str** | Custom prefix of entity identifiers in workspace | [optional] 
**settings** | [**[DeclarativeSetting]**](DeclarativeSetting.md) | A list of workspace settings. | [optional] 
**user_data_filters** | [**[DeclarativeUserDataFilter]**](DeclarativeUserDataFilter.md) | A list of workspace user data filters. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


