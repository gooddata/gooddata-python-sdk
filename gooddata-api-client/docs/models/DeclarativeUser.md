# gooddata_api_client.model.declarative_user.DeclarativeUser

A user and its properties

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A user and its properties | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | User identifier. | 
**authId** | str,  | str,  | User identification in the authentication manager. | [optional] 
**email** | str,  | str,  | User email address | [optional] 
**firstname** | str,  | str,  | User first name | [optional] 
**lastname** | str,  | str,  | User last name | [optional] 
**[permissions](#permissions)** | list, tuple,  | tuple,  |  | [optional] 
**[settings](#settings)** | list, tuple,  | tuple,  | A list of user settings. | [optional] 
**[userGroups](#userGroups)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# permissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeUserPermission**](DeclarativeUserPermission.md) | [**DeclarativeUserPermission**](DeclarativeUserPermission.md) | [**DeclarativeUserPermission**](DeclarativeUserPermission.md) |  | 

# settings

A list of user settings.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of user settings. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeSetting**](DeclarativeSetting.md) | [**DeclarativeSetting**](DeclarativeSetting.md) | [**DeclarativeSetting**](DeclarativeSetting.md) |  | 

# userGroups

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**UserGroupIdentifier**](UserGroupIdentifier.md) | [**UserGroupIdentifier**](UserGroupIdentifier.md) | [**UserGroupIdentifier**](UserGroupIdentifier.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

