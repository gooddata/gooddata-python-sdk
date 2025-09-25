# MeasureHeader


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | **str** | Format to be used to format the measure data. | [optional] 
**local_identifier** | **str** | Local identifier of the measure this header relates to. | 
**name** | **str** | Name of the measure. | [optional] 

## Example

```python
from gooddata_api_client.models.measure_header import MeasureHeader

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureHeader from a JSON string
measure_header_instance = MeasureHeader.from_json(json)
# print the JSON string representation of the object
print(MeasureHeader.to_json())

# convert the object into a dict
measure_header_dict = measure_header_instance.to_dict()
# create an instance of MeasureHeader from a dict
measure_header_from_dict = MeasureHeader.from_dict(measure_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


