# gooddata_api_client.model.metric_definition_override.MetricDefinitionOverride

(EXPERIMENTAL) Override for a catalog metric definition.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | (EXPERIMENTAL) Override for a catalog metric definition. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**item** | [**AfmObjectIdentifierCore**](AfmObjectIdentifierCore.md) | [**AfmObjectIdentifierCore**](AfmObjectIdentifierCore.md) |  | 
**definition** | [**InlineMeasureDefinition**](InlineMeasureDefinition.md) | [**InlineMeasureDefinition**](InlineMeasureDefinition.md) |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

