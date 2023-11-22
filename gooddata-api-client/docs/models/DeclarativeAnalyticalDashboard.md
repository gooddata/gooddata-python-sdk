# gooddata_api_client.model.declarative_analytical_dashboard.DeclarativeAnalyticalDashboard

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Analytical dashboard ID. | 
**title** | str,  | str,  | Analytical dashboard title. | 
**[content](#content)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom setting content in JSON format. | 
**description** | str,  | str,  | Analytical dashboard description. | [optional] 
**[permissions](#permissions)** | list, tuple,  | tuple,  | A list of permissions. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# content

Custom setting content in JSON format.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom setting content in JSON format. | 

# permissions

A list of permissions.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of permissions. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeAnalyticalDashboardPermission**](DeclarativeAnalyticalDashboardPermission.md) | [**DeclarativeAnalyticalDashboardPermission**](DeclarativeAnalyticalDashboardPermission.md) | [**DeclarativeAnalyticalDashboardPermission**](DeclarativeAnalyticalDashboardPermission.md) |  | 

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

