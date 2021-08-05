# DeclarativeWorkspaceDataFilter

Workspace Data Filters serving the filtering of what data users can see in workspaces.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Workspace Data Filters ID. This ID is further used to refer to this instance. | 
**title** | **str** | Workspace Data Filters title. | 
**column_name** | **str** | Workspace Data Filters column name. Data are filtered using this physical column. | 
**data_source_id** | **str** | Data source ID. Workspace Data Filters must always be connected to single data source. | 
**workspace_data_filter_settings** | [**[DeclarativeWorkspaceDataFilterSetting]**](DeclarativeWorkspaceDataFilterSetting.md) | Filter settings specifying values of filters valid for the workspace. | 
**description** | **str** | Workspace Data Filters description. | [optional] 
**workspace** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


