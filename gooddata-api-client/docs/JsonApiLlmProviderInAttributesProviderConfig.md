# JsonApiLlmProviderInAttributesProviderConfig

Provider-specific configuration including authentication.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**base_url** | **str** | Custom base URL for the Anthropic API. Defaults to the official endpoint; override only for enterprise proxies or compatible gateways. | [optional]  if omitted the server will use the default value of "https://api.anthropic.com"
**organization** | **str, none_type** | OpenAI organization ID. | [optional] 
**auth** | [**AnthropicProviderAuth**](AnthropicProviderAuth.md) |  | [optional] 
**type** | **str** | Provider type. | [optional]  if omitted the server will use the default value of "ANTHROPIC"
**endpoint** | **str** | Azure OpenAI endpoint URL. | [optional] 
**region** | **str** | AWS region for Bedrock. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


