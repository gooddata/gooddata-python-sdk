# ValidateLLMEndpointResponse


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**message** | **str** | Additional message about the LLM endpoint validation | 
**successful** | **bool** | Whether the LLM endpoint validation was successful | 

## Example

```python
from gooddata_api_client.models.validate_llm_endpoint_response import ValidateLLMEndpointResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateLLMEndpointResponse from a JSON string
validate_llm_endpoint_response_instance = ValidateLLMEndpointResponse.from_json(json)
# print the JSON string representation of the object
print(ValidateLLMEndpointResponse.to_json())

# convert the object into a dict
validate_llm_endpoint_response_dict = validate_llm_endpoint_response_instance.to_dict()
# create an instance of ValidateLLMEndpointResponse from a dict
validate_llm_endpoint_response_from_dict = ValidateLLMEndpointResponse.from_dict(validate_llm_endpoint_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


