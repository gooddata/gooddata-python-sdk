# MeasureGroupHeaders

Measure group headers

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure_group_headers** | [**List[MeasureHeader]**](MeasureHeader.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.measure_group_headers import MeasureGroupHeaders

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureGroupHeaders from a JSON string
measure_group_headers_instance = MeasureGroupHeaders.from_json(json)
# print the JSON string representation of the object
print(MeasureGroupHeaders.to_json())

# convert the object into a dict
measure_group_headers_dict = measure_group_headers_instance.to_dict()
# create an instance of MeasureGroupHeaders from a dict
measure_group_headers_from_dict = MeasureGroupHeaders.from_dict(measure_group_headers_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


