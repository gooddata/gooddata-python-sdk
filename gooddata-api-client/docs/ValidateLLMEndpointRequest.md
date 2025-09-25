# ValidateLLMEndpointRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**base_url** | **str** | Base URL for the LLM endpoint validation | [optional] 
**llm_model** | **str** | LLM model for the LLM endpoint validation | [optional] 
**llm_organization** | **str** | Organization name for the LLM endpoint validation | [optional] 
**provider** | **str** | Provider for the LLM endpoint validation | 
**token** | **str** | Token for the LLM endpoint validation | 

## Example

```python
from gooddata_api_client.models.validate_llm_endpoint_request import ValidateLLMEndpointRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ValidateLLMEndpointRequest from a JSON string
validate_llm_endpoint_request_instance = ValidateLLMEndpointRequest.from_json(json)
# print the JSON string representation of the object
print(ValidateLLMEndpointRequest.to_json())

# convert the object into a dict
validate_llm_endpoint_request_dict = validate_llm_endpoint_request_instance.to_dict()
# create an instance of ValidateLLMEndpointRequest from a dict
validate_llm_endpoint_request_from_dict = ValidateLLMEndpointRequest.from_dict(validate_llm_endpoint_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


