# JsonApiLlmEndpointInAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**title** | **str** | User-facing title of the LLM Provider. | 
**token** | **str** | The token to use to connect to the LLM provider. | 
**provider** | **str** | LLM Provider. | defaults to "OPENAI"
**base_url** | **str, none_type** | Custom LLM endpoint. | [optional] 
**description** | **str, none_type** | User-facing description of the LLM Provider. | [optional] 
**llm_model** | **str, none_type** | LLM Model. We provide a default model for each provider, but you can override it here. | [optional] 
**llm_organization** | **str, none_type** | Organization in LLM provider. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


