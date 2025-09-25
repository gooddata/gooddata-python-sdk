# JsonApiLlmEndpointPatchAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**base_url** | **str** | Custom LLM endpoint. | [optional] 
**llm_model** | **str** | LLM Model. We provide a default model for each provider, but you can override it here. | [optional] 
**llm_organization** | **str** | Organization in LLM provider. | [optional] 
**provider** | **str** | LLM Provider. | [optional] 
**title** | **str** | User-facing title of the LLM Provider. | [optional] 
**token** | **str** | The token to use to connect to the LLM provider. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_llm_endpoint_patch_attributes import JsonApiLlmEndpointPatchAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLlmEndpointPatchAttributes from a JSON string
json_api_llm_endpoint_patch_attributes_instance = JsonApiLlmEndpointPatchAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiLlmEndpointPatchAttributes.to_json())

# convert the object into a dict
json_api_llm_endpoint_patch_attributes_dict = json_api_llm_endpoint_patch_attributes_instance.to_dict()
# create an instance of JsonApiLlmEndpointPatchAttributes from a dict
json_api_llm_endpoint_patch_attributes_from_dict = JsonApiLlmEndpointPatchAttributes.from_dict(json_api_llm_endpoint_patch_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


