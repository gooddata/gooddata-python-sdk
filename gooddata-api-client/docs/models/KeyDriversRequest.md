# gooddata_api_client.model.key_drivers_request.KeyDriversRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**metric** | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 
**[auxMetrics](#auxMetrics)** | list, tuple,  | tuple,  | Additional metrics to be included in the computation, but excluded from the analysis. | [optional] 
**sortDirection** | str,  | str,  | Sorting elements - ascending/descending order. | [optional] must be one of ["ASC", "DESC", ] if omitted the server will use the default value of "DESC"
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# auxMetrics

Additional metrics to be included in the computation, but excluded from the analysis.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Additional metrics to be included in the computation, but excluded from the analysis. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

