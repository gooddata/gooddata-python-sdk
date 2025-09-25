# TotalResultHeader

Header containing the information related to a subtotal.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function** | **str** |  | 

## Example

```python
from gooddata_api_client.models.total_result_header import TotalResultHeader

# TODO update the JSON string below
json = "{}"
# create an instance of TotalResultHeader from a JSON string
total_result_header_instance = TotalResultHeader.from_json(json)
# print the JSON string representation of the object
print(TotalResultHeader.to_json())

# convert the object into a dict
total_result_header_dict = total_result_header_instance.to_dict()
# create an instance of TotalResultHeader from a dict
total_result_header_from_dict = TotalResultHeader.from_dict(total_result_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


