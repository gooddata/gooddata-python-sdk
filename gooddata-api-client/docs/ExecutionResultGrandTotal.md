# ExecutionResultGrandTotal

Contains the data of grand totals with the same dimensions.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **List[object]** | A multi-dimensional array of computed results. The most common one being a 2-dimensional array. The arrays can be composed of Double or null values. | 
**dimension_headers** | [**List[DimensionHeader]**](DimensionHeader.md) | Contains headers for a subset of &#x60;totalDimensions&#x60; in which the totals are grand totals. | 
**total_dimensions** | **List[str]** | Dimensions of the grand totals. | 

## Example

```python
from gooddata_api_client.models.execution_result_grand_total import ExecutionResultGrandTotal

# TODO update the JSON string below
json = "{}"
# create an instance of ExecutionResultGrandTotal from a JSON string
execution_result_grand_total_instance = ExecutionResultGrandTotal.from_json(json)
# print the JSON string representation of the object
print(ExecutionResultGrandTotal.to_json())

# convert the object into a dict
execution_result_grand_total_dict = execution_result_grand_total_instance.to_dict()
# create an instance of ExecutionResultGrandTotal from a dict
execution_result_grand_total_from_dict = ExecutionResultGrandTotal.from_dict(execution_result_grand_total_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


