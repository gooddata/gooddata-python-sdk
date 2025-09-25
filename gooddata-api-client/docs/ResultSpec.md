# ResultSpec

Specifies how the result data will be formatted (```dimensions```) and which additional data shall be computed (```totals```).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimensions** | [**List[Dimension]**](Dimension.md) |  | 
**totals** | [**List[Total]**](Total.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.result_spec import ResultSpec

# TODO update the JSON string below
json = "{}"
# create an instance of ResultSpec from a JSON string
result_spec_instance = ResultSpec.from_json(json)
# print the JSON string representation of the object
print(ResultSpec.to_json())

# convert the object into a dict
result_spec_dict = result_spec_instance.to_dict()
# create an instance of ResultSpec from a dict
result_spec_from_dict = ResultSpec.from_dict(result_spec_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


