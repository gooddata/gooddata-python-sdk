# gooddata_api_client.model.relative_bounded_date_filter.RelativeBoundedDateFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**granularity** | str,  | str,  |  | must be one of ["ALL_TIME_GRANULARITY", "GDC.time.year", "GDC.time.week_us", "GDC.time.week_in_year", "GDC.time.week_in_quarter", "GDC.time.week", "GDC.time.euweek_in_year", "GDC.time.euweek_in_quarter", "GDC.time.quarter", "GDC.time.quarter_in_year", "GDC.time.month", "GDC.time.month_in_quarter", "GDC.time.month_in_year", "GDC.time.day_in_year", "GDC.time.day_in_quarter", "GDC.time.day_in_month", "GDC.time.day_in_week", "GDC.time.day_in_euweek", "GDC.time.date", "GDC.time.hour", "GDC.time.hour_in_day", "GDC.time.minute", "GDC.time.minute_in_hour", "GDC.time.fiscal_month", "GDC.time.fiscal_quarter", "GDC.time.fiscal_year", ] 
**from** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 32 bit integer
**to** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 32 bit integer
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

