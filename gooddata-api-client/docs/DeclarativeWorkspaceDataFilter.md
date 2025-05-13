# DeclarativeWorkspaceDataFilter

Workspace Data Filters serving the filtering of what data users can see in workspaces.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column_name** | **str** | Workspace Data Filters column name. Data are filtered using this physical column. | 
**id** | **str** | Workspace Data Filters ID. This ID is further used to refer to this instance. | 
**title** | **str** | Workspace Data Filters title. | 
**workspace** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | 
**workspace_data_filter_settings** | [**[DeclarativeWorkspaceDataFilterSetting]**](DeclarativeWorkspaceDataFilterSetting.md) | Filter settings specifying values of filters valid for the workspace. | 
**description** | **str** | Workspace Data Filters description. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


