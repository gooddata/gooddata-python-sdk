# DimensionHeader

Contains the dimension-specific header information.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**header_groups** | [**List[HeaderGroup]**](HeaderGroup.md) | An array containing header groups. | 

## Example

```python
from gooddata_api_client.models.dimension_header import DimensionHeader

# TODO update the JSON string below
json = "{}"
# create an instance of DimensionHeader from a JSON string
dimension_header_instance = DimensionHeader.from_json(json)
# print the JSON string representation of the object
print(DimensionHeader.to_json())

# convert the object into a dict
dimension_header_dict = dimension_header_instance.to_dict()
# create an instance of DimensionHeader from a dict
dimension_header_from_dict = DimensionHeader.from_dict(dimension_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


