# gooddata_api_client.model.json_api_llm_provider_in.JsonApiLlmProviderIn

LLM Provider configuration for connecting to LLM services.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | LLM Provider configuration for connecting to LLM services. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attributes](#attributes)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**id** | str,  | str,  | API identifier of an object | 
**type** | str,  | str,  | Object type | must be one of ["llmProvider", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[models](#models)** | list, tuple, None,  | tuple, NoneClass,  | List of LLM models available for this provider. | 
**[providerConfig](#providerConfig)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Provider-specific configuration including authentication. | 
**defaultModelId** | None, str,  | NoneClass, str,  | ID of the default model to use from the models list. | [optional] 
**description** | None, str,  | NoneClass, str,  | Description of the LLM Provider. | [optional] 
**name** | None, str,  | NoneClass, str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# models

List of LLM models available for this provider.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  | List of LLM models available for this provider. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict,  | frozendict.frozendict,  | LLM Model configuration (id, family) within a provider. | 

# items

LLM Model configuration (id, family) within a provider.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | LLM Model configuration (id, family) within a provider. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Unique identifier of the model (e.g., gpt-5.3, claude-4.6). | 
**family** | str,  | str,  | Family of LLM models. | must be one of ["OPENAI", "ANTHROPIC", "META", "MISTRAL", "AMAZON", "GOOGLE", "COHERE", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# providerConfig

Provider-specific configuration including authentication.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Provider-specific configuration including authentication. | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AwsBedrockProviderConfig](AwsBedrockProviderConfig.md) | [**AwsBedrockProviderConfig**](AwsBedrockProviderConfig.md) | [**AwsBedrockProviderConfig**](AwsBedrockProviderConfig.md) |  | 
[AzureFoundryProviderConfig](AzureFoundryProviderConfig.md) | [**AzureFoundryProviderConfig**](AzureFoundryProviderConfig.md) | [**AzureFoundryProviderConfig**](AzureFoundryProviderConfig.md) |  | 
[OpenAIProviderConfig](OpenAIProviderConfig.md) | [**OpenAIProviderConfig**](OpenAIProviderConfig.md) | [**OpenAIProviderConfig**](OpenAIProviderConfig.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

