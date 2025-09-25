# ExecutionResultHeader

Abstract execution result header

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_header** | [**AttributeResultHeader**](AttributeResultHeader.md) |  | 
**measure_header** | [**MeasureResultHeader**](MeasureResultHeader.md) |  | 
**total_header** | [**TotalResultHeader**](TotalResultHeader.md) |  | 

## Example

```python
from gooddata_api_client.models.execution_result_header import ExecutionResultHeader

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionResultHeader from a JSON string
execution_result_header_instance = ExecutionResultHeader.from_json(json)
# print the JSON string representation of the object
print(ExecutionResultHeader.to_json())

# convert the object into a dict
execution_result_header_dict = execution_result_header_instance.to_dict()
# create an instance of ExecutionResultHeader from a dict
execution_result_header_from_dict = ExecutionResultHeader.from_dict(execution_result_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


