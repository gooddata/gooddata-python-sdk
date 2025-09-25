# MeasureExecutionResultHeader


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure_header** | [**MeasureResultHeader**](MeasureResultHeader.md) |  | 

## Example

```python
from gooddata_api_client.models.measure_execution_result_header import MeasureExecutionResultHeader

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureExecutionResultHeader from a JSON string
measure_execution_result_header_instance = MeasureExecutionResultHeader.from_json(json)
# print the JSON string representation of the object
print(MeasureExecutionResultHeader.to_json())

# convert the object into a dict
measure_execution_result_header_dict = measure_execution_result_header_instance.to_dict()
# create an instance of MeasureExecutionResultHeader from a dict
measure_execution_result_header_from_dict = MeasureExecutionResultHeader.from_dict(measure_execution_result_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


