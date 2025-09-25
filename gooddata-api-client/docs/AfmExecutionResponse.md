# AfmExecutionResponse

Response to AFM execution request

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**execution_response** | [**ExecutionResponse**](ExecutionResponse.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_execution_response import AfmExecutionResponse

# TODO update the JSON string below
json = "{}"
# create an instance of AfmExecutionResponse from a JSON string
afm_execution_response_instance = AfmExecutionResponse.from_json(json)
# print the JSON string representation of the object
print(AfmExecutionResponse.to_json())

# convert the object into a dict
afm_execution_response_dict = afm_execution_response_instance.to_dict()
# create an instance of AfmExecutionResponse from a dict
afm_execution_response_from_dict = AfmExecutionResponse.from_dict(afm_execution_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


