# gooddata_api_client.model.test_llm_provider_definition_request.TestLlmProviderDefinitionRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[providerConfig](#providerConfig)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 
**[models](#models)** | list, tuple,  | tuple,  | Models to test. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# providerConfig

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AwsBedrockProviderConfig](AwsBedrockProviderConfig.md) | [**AwsBedrockProviderConfig**](AwsBedrockProviderConfig.md) | [**AwsBedrockProviderConfig**](AwsBedrockProviderConfig.md) |  | 
[AzureFoundryProviderConfig](AzureFoundryProviderConfig.md) | [**AzureFoundryProviderConfig**](AzureFoundryProviderConfig.md) | [**AzureFoundryProviderConfig**](AzureFoundryProviderConfig.md) |  | 
[OpenAIProviderConfig](OpenAIProviderConfig.md) | [**OpenAIProviderConfig**](OpenAIProviderConfig.md) | [**OpenAIProviderConfig**](OpenAIProviderConfig.md) |  | 

# models

Models to test.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Models to test. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**LlmModel**](LlmModel.md) | [**LlmModel**](LlmModel.md) | [**LlmModel**](LlmModel.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

