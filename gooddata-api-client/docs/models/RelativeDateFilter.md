# gooddata_api_client.model.relative_date_filter.RelativeDateFilter

A date filter specifying a time interval that is relative to the current date. For example, last week, next month, and so on. Field dataset is representing qualifier of date dimension.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A date filter specifying a time interval that is relative to the current date. For example, last week, next month, and so on. Field dataset is representing qualifier of date dimension. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[relativeDateFilter](#relativeDateFilter)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# relativeDateFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**granularity** | str,  | str,  | Date granularity specifying particular date attribute in given dimension. | must be one of ["MINUTE", "HOUR", "DAY", "WEEK", "MONTH", "QUARTER", "YEAR", "MINUTE_OF_HOUR", "HOUR_OF_DAY", "DAY_OF_WEEK", "DAY_OF_MONTH", "DAY_OF_YEAR", "WEEK_OF_YEAR", "MONTH_OF_YEAR", "QUARTER_OF_YEAR", ] 
**from** | decimal.Decimal, int,  | decimal.Decimal,  | Start of the filtering interval. Specified by number of periods (with respect to given granularity). Typically negative (historical time interval like -2 for &#x27;2 days/weeks, ... ago&#x27;). | value must be a 32 bit integer
**to** | decimal.Decimal, int,  | decimal.Decimal,  | End of the filtering interval. Specified by number of periods (with respect to given granularity). Value &#x27;O&#x27; is representing current time-interval (current day, week, ...). | value must be a 32 bit integer
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**applyOnResult** | bool,  | BoolClass,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

