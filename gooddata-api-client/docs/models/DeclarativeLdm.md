# gooddata_api_client.model.declarative_ldm.DeclarativeLdm

A logical data model (LDM) representation.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A logical data model (LDM) representation. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[datasets](#datasets)** | list, tuple,  | tuple,  | An array containing datasets. | [optional] 
**[dateInstances](#dateInstances)** | list, tuple,  | tuple,  | An array containing date-related datasets. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# datasets

An array containing datasets.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array containing datasets. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeDataset**](DeclarativeDataset.md) | [**DeclarativeDataset**](DeclarativeDataset.md) | [**DeclarativeDataset**](DeclarativeDataset.md) |  | 

# dateInstances

An array containing date-related datasets.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array containing date-related datasets. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeDateDataset**](DeclarativeDateDataset.md) | [**DeclarativeDateDataset**](DeclarativeDateDataset.md) | [**DeclarativeDateDataset**](DeclarativeDateDataset.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

