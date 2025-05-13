# ExecutionResult

Contains the result of an AFM execution.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **[{str: (bool, date, datetime, dict, float, int, list, str, none_type)}]** | A multi-dimensional array of computed results. The most common one being a 2-dimensional array. The arrays can be composed of Double or null values. | 
**dimension_headers** | [**[DimensionHeader]**](DimensionHeader.md) | An array containing dimension headers. The size of the array corresponds to the number of dimensions. Their order corresponds to the dimension order in the execution result spec. | 
**grand_totals** | [**[ExecutionResultGrandTotal]**](ExecutionResultGrandTotal.md) |  | 
**metadata** | [**ExecutionResultMetadata**](ExecutionResultMetadata.md) |  | 
**paging** | [**ExecutionResultPaging**](ExecutionResultPaging.md) |  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


