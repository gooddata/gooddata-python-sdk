# ResultDimension

Single result dimension

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**headers** | [**List[ResultDimensionHeader]**](ResultDimensionHeader.md) |  | 
**local_identifier** | **str** | Local identifier of the dimension. | 

## Example

```python
from gooddata_api_client.models.result_dimension import ResultDimension

# TODO update the JSON string below
json = "{}"
# create an instance of ResultDimension from a JSON string
result_dimension_instance = ResultDimension.from_json(json)
# print the JSON string representation of the object
print(ResultDimension.to_json())

# convert the object into a dict
result_dimension_dict = result_dimension_instance.to_dict()
# create an instance of ResultDimension from a dict
result_dimension_from_dict = ResultDimension.from_dict(result_dimension_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


