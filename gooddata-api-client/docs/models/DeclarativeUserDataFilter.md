# gooddata_api_client.model.declarative_user_data_filter.DeclarativeUserDataFilter

User Data Filters serving the filtering of what data users can see in workspaces.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | User Data Filters serving the filtering of what data users can see in workspaces. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | User Data Filters ID. This ID is further used to refer to this instance. | 
**maql** | str,  | str,  | Expression in MAQL specifying the User Data Filter | 
**title** | str,  | str,  | User Data Filters setting title. | 
**description** | str,  | str,  | User Data Filters setting description. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**user** | [**UserIdentifier**](UserIdentifier.md) | [**UserIdentifier**](UserIdentifier.md) |  | [optional] 
**userGroup** | [**UserGroupIdentifier**](UserGroupIdentifier.md) | [**UserGroupIdentifier**](UserGroupIdentifier.md) |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# tags

A list of tags.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of tags. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | A list of tags. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

