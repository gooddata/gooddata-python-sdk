# gooddata_api_client.model.declarative_organization.DeclarativeOrganization

Complete definition of an organization in a declarative form.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Complete definition of an organization in a declarative form. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**organization** | [**DeclarativeOrganizationInfo**](DeclarativeOrganizationInfo.md) | [**DeclarativeOrganizationInfo**](DeclarativeOrganizationInfo.md) |  | 
**[dataSources](#dataSources)** | list, tuple,  | tuple,  |  | [optional] 
**[userGroups](#userGroups)** | list, tuple,  | tuple,  |  | [optional] 
**[users](#users)** | list, tuple,  | tuple,  |  | [optional] 
**[workspaceDataFilters](#workspaceDataFilters)** | list, tuple,  | tuple,  |  | [optional] 
**[workspaces](#workspaces)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# dataSources

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeDataSource**](DeclarativeDataSource.md) | [**DeclarativeDataSource**](DeclarativeDataSource.md) | [**DeclarativeDataSource**](DeclarativeDataSource.md) |  | 

# userGroups

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeUserGroup**](DeclarativeUserGroup.md) | [**DeclarativeUserGroup**](DeclarativeUserGroup.md) | [**DeclarativeUserGroup**](DeclarativeUserGroup.md) |  | 

# users

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeUser**](DeclarativeUser.md) | [**DeclarativeUser**](DeclarativeUser.md) | [**DeclarativeUser**](DeclarativeUser.md) |  | 

# workspaceDataFilters

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeWorkspaceDataFilter**](DeclarativeWorkspaceDataFilter.md) | [**DeclarativeWorkspaceDataFilter**](DeclarativeWorkspaceDataFilter.md) | [**DeclarativeWorkspaceDataFilter**](DeclarativeWorkspaceDataFilter.md) |  | 

# workspaces

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeWorkspace**](DeclarativeWorkspace.md) | [**DeclarativeWorkspace**](DeclarativeWorkspace.md) | [**DeclarativeWorkspace**](DeclarativeWorkspace.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

