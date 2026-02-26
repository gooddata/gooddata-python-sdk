# gooddata_api_client.model.forecast_request.ForecastRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**forecastPeriod** | decimal.Decimal, int,  | decimal.Decimal,  | Number of future periods that should be forecasted | value must be a 32 bit integer
**confidenceLevel** | decimal.Decimal, int, float,  | decimal.Decimal,  | Confidence interval boundary value. | [optional] if omitted the server will use the default value of 0.95value must be a 32 bit float
**seasonal** | bool,  | BoolClass,  | Whether the input data is seasonal | [optional] if omitted the server will use the default value of False
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

