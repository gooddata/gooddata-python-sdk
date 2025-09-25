# ResultDimensionHeader

One of the headers in a result dimension.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure_group_headers** | [**List[MeasureHeader]**](MeasureHeader.md) |  | [optional] 
**attribute_header** | [**AttributeHeaderAttributeHeader**](AttributeHeaderAttributeHeader.md) |  | 

## Example

```python
from gooddata_api_client.models.result_dimension_header import ResultDimensionHeader

# TODO update the JSON string below
json = "{}"
# create an instance of ResultDimensionHeader from a JSON string
result_dimension_header_instance = ResultDimensionHeader.from_json(json)
# print the JSON string representation of the object
print(ResultDimensionHeader.to_json())

# convert the object into a dict
result_dimension_header_dict = result_dimension_header_instance.to_dict()
# create an instance of ResultDimensionHeader from a dict
result_dimension_header_from_dict = ResultDimensionHeader.from_dict(result_dimension_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


