# gooddata_api_client.model.simple_measure_definition.SimpleMeasureDefinition

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[measure](#measure)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# measure

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**item** | [**AfmObjectIdentifierCore**](AfmObjectIdentifierCore.md) | [**AfmObjectIdentifierCore**](AfmObjectIdentifierCore.md) |  | 
**aggregation** | str,  | str,  | Definition of aggregation type of the metric. | [optional] must be one of ["SUM", "COUNT", "AVG", "MIN", "MAX", "MEDIAN", "RUNSUM", "APPROXIMATE_COUNT", ] 
**computeRatio** | bool,  | BoolClass,  | If true compute the percentage of given metric values (broken down by AFM attributes) to the total (not broken down). | [optional] if omitted the server will use the default value of False
**[filters](#filters)** | list, tuple,  | tuple,  | Metrics can be filtered by attribute filters with the same interface as ones for global AFM. Note that only one DateFilter is allowed. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# filters

Metrics can be filtered by attribute filters with the same interface as ones for global AFM. Note that only one DateFilter is allowed.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Metrics can be filtered by attribute filters with the same interface as ones for global AFM. Note that only one DateFilter is allowed. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**FilterDefinitionForSimpleMeasure**](FilterDefinitionForSimpleMeasure.md) | [**FilterDefinitionForSimpleMeasure**](FilterDefinitionForSimpleMeasure.md) | [**FilterDefinitionForSimpleMeasure**](FilterDefinitionForSimpleMeasure.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

