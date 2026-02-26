# gooddata_api_client.model.aws_bedrock_provider_config.AwsBedrockProviderConfig

Configuration for AWS Bedrock provider.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Configuration for AWS Bedrock provider. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**auth** | [**BedrockProviderAuth**](BedrockProviderAuth.md) | [**BedrockProviderAuth**](BedrockProviderAuth.md) |  | 
**region** | str,  | str,  | AWS region for Bedrock. | 
**type** | str,  | str,  | Provider type. | must be one of ["AWS_BEDROCK", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

