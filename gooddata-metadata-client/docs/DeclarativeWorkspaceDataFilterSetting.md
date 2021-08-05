# DeclarativeWorkspaceDataFilterSetting

Workspace Data Filters serving the filtering of what data users can see in workspaces.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Workspace Data Filters ID. This ID is further used to refer to this instance. | 
**title** | **str** | Workspace Data Filters setting title. | 
**filter_values** | **[str]** | Only those rows are returned, where columnName from filter matches those values. | 
**workspace** | [**WorkspaceIdentifier**](WorkspaceIdentifier.md) |  | 
**description** | **str** | Workspace Data Filters setting description. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


