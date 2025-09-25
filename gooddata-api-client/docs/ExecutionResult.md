# ExecutionResult

Contains the result of an AFM execution.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **List[object]** | A multi-dimensional array of computed results. The most common one being a 2-dimensional array. The arrays can be composed of Double or null values. | 
**dimension_headers** | [**List[DimensionHeader]**](DimensionHeader.md) | An array containing dimension headers. The size of the array corresponds to the number of dimensions. Their order corresponds to the dimension order in the execution result spec. | 
**grand_totals** | [**List[ExecutionResultGrandTotal]**](ExecutionResultGrandTotal.md) |  | 
**metadata** | [**ExecutionResultMetadata**](ExecutionResultMetadata.md) |  | 
**paging** | [**ExecutionResultPaging**](ExecutionResultPaging.md) |  | 

## Example

```python
from gooddata_api_client.models.execution_result import ExecutionResult

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionResult from a JSON string
execution_result_instance = ExecutionResult.from_json(json)
# print the JSON string representation of the object
print(ExecutionResult.to_json())

# convert the object into a dict
execution_result_dict = execution_result_instance.to_dict()
# create an instance of ExecutionResult from a dict
execution_result_from_dict = ExecutionResult.from_dict(execution_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


