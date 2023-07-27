# gooddata_api_client.model.total.Total

Definition of a total. There are two types of totals: grand totals and subtotals. Grand total data will be returned in a separate section of the result structure while subtotals are fully integrated into the main result data. The mechanism for this distinction is automatic and it's described in `TotalDimension`

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Definition of a total. There are two types of totals: grand totals and subtotals. Grand total data will be returned in a separate section of the result structure while subtotals are fully integrated into the main result data. The mechanism for this distinction is automatic and it&#x27;s described in &#x60;TotalDimension&#x60; | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**metric** | str,  | str,  | The metric for which the total will be computed | 
**[totalDimensions](#totalDimensions)** | list, tuple,  | tuple,  |  | 
**function** | str,  | str,  | Aggregation function to compute the total. | must be one of ["SUM", "MIN", "MAX", "AVG", "MED", ] 
**localIdentifier** | str,  | str,  | Total identification within this request. Used e.g. in sorting by a total. | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# totalDimensions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**TotalDimension**](TotalDimension.md) | [**TotalDimension**](TotalDimension.md) | [**TotalDimension**](TotalDimension.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

