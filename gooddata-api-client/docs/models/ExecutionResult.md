# gooddata_api_client.model.execution_result.ExecutionResult

Contains the result of an AFM execution.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Contains the result of an AFM execution. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[data](#data)** | list, tuple,  | tuple,  | A multi-dimensional array of computed results. The most common one being a 2-dimensional array. The arrays can be composed of Double or null values. | 
**[dimensionHeaders](#dimensionHeaders)** | list, tuple,  | tuple,  | An array containing dimension headers. The size of the array corresponds to the number of dimensions. Their order corresponds to the dimension order in the execution result spec. | 
**paging** | [**ExecutionResultPaging**](ExecutionResultPaging.md) | [**ExecutionResultPaging**](ExecutionResultPaging.md) |  | 
**[grandTotals](#grandTotals)** | list, tuple,  | tuple,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# data

A multi-dimensional array of computed results. The most common one being a 2-dimensional array. The arrays can be composed of Double or null values.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A multi-dimensional array of computed results. The most common one being a 2-dimensional array. The arrays can be composed of Double or null values. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# dimensionHeaders

An array containing dimension headers. The size of the array corresponds to the number of dimensions. Their order corresponds to the dimension order in the execution result spec.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array containing dimension headers. The size of the array corresponds to the number of dimensions. Their order corresponds to the dimension order in the execution result spec. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DimensionHeader**](DimensionHeader.md) | [**DimensionHeader**](DimensionHeader.md) | [**DimensionHeader**](DimensionHeader.md) |  | 

# grandTotals

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExecutionResultGrandTotal**](ExecutionResultGrandTotal.md) | [**ExecutionResultGrandTotal**](ExecutionResultGrandTotal.md) | [**ExecutionResultGrandTotal**](ExecutionResultGrandTotal.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

