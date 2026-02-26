# gooddata_api_client.model.forecast_config.ForecastConfig

Forecast configuration.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Forecast configuration. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**confidenceLevel** | decimal.Decimal, int, float,  | decimal.Decimal,  | Confidence interval boundary value. | value must be a 32 bit float
**seasonal** | bool,  | BoolClass,  | Whether the input data is seasonal | 
**forecastPeriod** | decimal.Decimal, int,  | decimal.Decimal,  | Number of future periods that should be forecasted | value must be a 32 bit integer
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

