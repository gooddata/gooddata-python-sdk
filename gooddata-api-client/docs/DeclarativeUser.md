# DeclarativeUser

A user and its properties

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | User identifier. | 
**auth_id** | **str** | User identification in the authentication manager. | [optional] 
**email** | **str** | User email address | [optional] 
**firstname** | **str** | User first name | [optional] 
**lastname** | **str** | User last name | [optional] 
**permissions** | [**[DeclarativeUserPermission]**](DeclarativeUserPermission.md) |  | [optional] 
**settings** | [**[DeclarativeSetting]**](DeclarativeSetting.md) | A list of user settings. | [optional] 
**user_groups** | [**[DeclarativeUserGroupIdentifier]**](DeclarativeUserGroupIdentifier.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


