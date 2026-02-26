# gooddata_api_client.model.all_time_date_filter.AllTimeDateFilter

An all-time date filter that does not restrict by date range. Controls how rows with empty (null/missing) date values are handled.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | An all-time date filter that does not restrict by date range. Controls how rows with empty (null/missing) date values are handled. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[allTimeDateFilter](#allTimeDateFilter)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# allTimeDateFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**applyOnResult** | bool,  | BoolClass,  |  | [optional] 
**emptyValueHandling** | str,  | str,  | Specifies how rows with empty (null/missing) date values should be handled. INCLUDE means no filtering effect (default), EXCLUDE removes rows with null dates, ONLY keeps only rows with null dates. | [optional] must be one of ["INCLUDE", "EXCLUDE", "ONLY", ] if omitted the server will use the default value of "INCLUDE"
**granularity** | str,  | str,  | Date granularity used to resolve the date attribute label for null value checks. Defaults to DAY if not specified. | [optional] must be one of ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR", "MINUTE_OF_HOUR", "HOUR_OF_DAY", "DAY_OF_WEEK", "DAY_OF_MONTH", "DAY_OF_QUARTER", "DAY_OF_YEAR", "WEEK_OF_YEAR", "MONTH_OF_YEAR", "QUARTER_OF_YEAR", "FISCAL_MONTH", "FISCAL_QUARTER", "FISCAL_YEAR", ] if omitted the server will use the default value of "DAY"
**localIdentifier** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

