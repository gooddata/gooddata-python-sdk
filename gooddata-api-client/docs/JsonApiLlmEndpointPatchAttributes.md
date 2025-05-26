# JsonApiLlmEndpointPatchAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**base_url** | **str, none_type** | Custom LLM endpoint. | [optional] 
**description** | **str, none_type** | User-facing description of the LLM Provider. | [optional] 
**llm_model** | **str** | LLM Model. We provide a default model for each provider, but you can override it here. | [optional] 
**llm_organization** | **str, none_type** | Organization in LLM provider. | [optional] 
**provider** | **str** | LLM Provider. | [optional]  if omitted the server will use the default value of "OPENAI"
**title** | **str** | User-facing title of the LLM Provider. | [optional] 
**token** | **str** | The token to use to connect to the LLM provider. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


