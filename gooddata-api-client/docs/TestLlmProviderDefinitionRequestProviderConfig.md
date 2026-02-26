# TestLlmProviderDefinitionRequestProviderConfig


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**base_url** | **str, none_type** | Custom base URL for OpenAI API. | [optional]  if omitted the server will use the default value of "https://api.openai.com"
**organization** | **str, none_type** | OpenAI organization ID. | [optional] 
**auth** | [**OpenAiProviderAuth**](OpenAiProviderAuth.md) |  | [optional] 
**region** | **str** | AWS region for Bedrock. | [optional] 
**type** | **str** | Provider type. | [optional]  if omitted the server will use the default value of "OPENAI"
**endpoint** | **str** | Azure AI inference endpoint URL. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


