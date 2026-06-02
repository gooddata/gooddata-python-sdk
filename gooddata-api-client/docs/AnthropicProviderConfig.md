# AnthropicProviderConfig

Configuration for Anthropic provider.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**auth** | [**AnthropicProviderAuth**](AnthropicProviderAuth.md) |  | 
**type** | **str** | Provider type. | defaults to "ANTHROPIC"
**base_url** | **str** | Custom base URL for the Anthropic API. Defaults to the official endpoint; override only for enterprise proxies or compatible gateways. | [optional]  if omitted the server will use the default value of "https://api.anthropic.com"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


