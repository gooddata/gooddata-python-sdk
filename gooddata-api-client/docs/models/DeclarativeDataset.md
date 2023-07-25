# gooddata_api_client.model.declarative_dataset.DeclarativeDataset

A dataset defined by its properties.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A dataset defined by its properties. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[references](#references)** | list, tuple,  | tuple,  | An array of references. | 
**[grain](#grain)** | list, tuple,  | tuple,  | An array of grain identifiers. | 
**id** | str,  | str,  | The Dataset ID. This ID is further used to refer to this instance of dataset. | 
**title** | str,  | str,  | A dataset title. | 
**[attributes](#attributes)** | list, tuple,  | tuple,  | An array of attributes. | [optional] 
**dataSourceTableId** | [**DataSourceTableIdentifier**](DataSourceTableIdentifier.md) | [**DataSourceTableIdentifier**](DataSourceTableIdentifier.md) |  | [optional] 
**description** | str,  | str,  | A dataset description. | [optional] 
**[facts](#facts)** | list, tuple,  | tuple,  | An array of facts. | [optional] 
**sql** | [**DeclarativeDatasetSql**](DeclarativeDatasetSql.md) | [**DeclarativeDatasetSql**](DeclarativeDatasetSql.md) |  | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**[workspaceDataFilterColumns](#workspaceDataFilterColumns)** | list, tuple,  | tuple,  | An array of workspace data filter columns applied on a workspace. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# grain

An array of grain identifiers.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of grain identifiers. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**GrainIdentifier**](GrainIdentifier.md) | [**GrainIdentifier**](GrainIdentifier.md) | [**GrainIdentifier**](GrainIdentifier.md) |  | 

# references

An array of references.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of references. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeReference**](DeclarativeReference.md) | [**DeclarativeReference**](DeclarativeReference.md) | [**DeclarativeReference**](DeclarativeReference.md) |  | 

# attributes

An array of attributes.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of attributes. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeAttribute**](DeclarativeAttribute.md) | [**DeclarativeAttribute**](DeclarativeAttribute.md) | [**DeclarativeAttribute**](DeclarativeAttribute.md) |  | 

# facts

An array of facts.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of facts. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeFact**](DeclarativeFact.md) | [**DeclarativeFact**](DeclarativeFact.md) | [**DeclarativeFact**](DeclarativeFact.md) |  | 

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

# workspaceDataFilterColumns

An array of workspace data filter columns applied on a workspace.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of workspace data filter columns applied on a workspace. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeWorkspaceDataFilterColumn**](DeclarativeWorkspaceDataFilterColumn.md) | [**DeclarativeWorkspaceDataFilterColumn**](DeclarativeWorkspaceDataFilterColumn.md) | [**DeclarativeWorkspaceDataFilterColumn**](DeclarativeWorkspaceDataFilterColumn.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

