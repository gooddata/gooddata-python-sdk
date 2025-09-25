# AttributeExecutionResultHeader


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_header** | [**AttributeResultHeader**](AttributeResultHeader.md) |  | 

## Example

```python
from gooddata_api_client.models.attribute_execution_result_header import AttributeExecutionResultHeader

# TODO update the JSON string below
json = "{}"
# create an instance of AttributeExecutionResultHeader from a JSON string
attribute_execution_result_header_instance = AttributeExecutionResultHeader.from_json(json)
# print the JSON string representation of the object
print(AttributeExecutionResultHeader.to_json())

# convert the object into a dict
attribute_execution_result_header_dict = attribute_execution_result_header_instance.to_dict()
# create an instance of AttributeExecutionResultHeader from a dict
attribute_execution_result_header_from_dict = AttributeExecutionResultHeader.from_dict(attribute_execution_result_header_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


