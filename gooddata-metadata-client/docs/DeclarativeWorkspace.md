# DeclarativeWorkspace

A declarative form of a particular workspace.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of a workspace | 
**name** | **str** | Name of a workspace to view. | 
**early_access** | **str** | Early access defined on level Workspace | [optional] 
**hierarchy_permissions** | [**[DeclarativeWorkspaceHierarchyPermission]**](DeclarativeWorkspaceHierarchyPermission.md) |  | [optional] 
**model** | [**DeclarativeWorkspaceModel**](DeclarativeWorkspaceModel.md) |  | [optional] 
**parent** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | [optional] 
**permissions** | [**[DeclarativeSingleWorkspacePermission]**](DeclarativeSingleWorkspacePermission.md) |  | [optional] 
**settings** | [**[DeclarativeSetting]**](DeclarativeSetting.md) | A list of workspace settings. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


