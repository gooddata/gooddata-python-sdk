# gooddata_api_client.model.declarative_user_group.DeclarativeUserGroup

A user-group and its properties

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A user-group and its properties | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | UserGroup identifier. | 
**name** | str,  | str,  | Name of UserGroup | [optional] 
**[parents](#parents)** | list, tuple,  | tuple,  |  | [optional] 
**[permissions](#permissions)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# parents

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**UserGroupIdentifier**](UserGroupIdentifier.md) | [**UserGroupIdentifier**](UserGroupIdentifier.md) | [**UserGroupIdentifier**](UserGroupIdentifier.md) |  | 

# permissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeUserGroupPermission**](DeclarativeUserGroupPermission.md) | [**DeclarativeUserGroupPermission**](DeclarativeUserGroupPermission.md) | [**DeclarativeUserGroupPermission**](DeclarativeUserGroupPermission.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

