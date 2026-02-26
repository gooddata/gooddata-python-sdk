# gooddata_api_client.model.azure_foundry_provider_config.AzureFoundryProviderConfig

Configuration for Azure Foundry provider.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Configuration for Azure Foundry provider. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**endpoint** | str,  | str,  | Azure AI inference endpoint URL. | 
**auth** | [**AzureFoundryProviderAuth**](AzureFoundryProviderAuth.md) | [**AzureFoundryProviderAuth**](AzureFoundryProviderAuth.md) |  | 
**type** | str,  | str,  | Provider type. | must be one of ["AZURE_FOUNDRY", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

