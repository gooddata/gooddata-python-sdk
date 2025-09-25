# MeasureResultHeader

Header containing the information related to metrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure_index** | **int** | Metric index. Starts at 0. | 

## Example

```python
from gooddata_api_client.models.measure_result_header import MeasureResultHeader

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureResultHeader from a JSON string
measure_result_header_instance = MeasureResultHeader.from_json(json)
# print the JSON string representation of the object
print(MeasureResultHeader.to_json())

# convert the object into a dict
measure_result_header_dict = measure_result_header_instance.to_dict()
# create an instance of MeasureResultHeader from a dict
measure_result_header_from_dict = MeasureResultHeader.from_dict(measure_result_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


