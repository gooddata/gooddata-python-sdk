# gooddata_api_client.model.open_ai_provider_config.OpenAIProviderConfig

Configuration for OpenAI provider.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Configuration for OpenAI provider. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**auth** | [**OpenAiProviderAuth**](OpenAiProviderAuth.md) | [**OpenAiProviderAuth**](OpenAiProviderAuth.md) |  | 
**type** | str,  | str,  | Provider type. | must be one of ["OPENAI", ] 
**baseUrl** | None, str,  | NoneClass, str,  | Custom base URL for OpenAI API. | [optional] if omitted the server will use the default value of "https://api.openai.com"
**organization** | None, str,  | NoneClass, str,  | OpenAI organization ID. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

