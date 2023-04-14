# DeclarativeUserDataFilter

User Data Filters serving the filtering of what data users can see in workspaces.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | User Data Filters ID. This ID is further used to refer to this instance. | 
**maql** | **str** | Expression in MAQL specifying the User Data Filter | 
**title** | **str** | User Data Filters setting title. | 
**description** | **str** | User Data Filters setting description. | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**user** | [**UserIdentifier**](UserIdentifier.md) |  | [optional] 
**user_group** | [**UserGroupIdentifier**](UserGroupIdentifier.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


