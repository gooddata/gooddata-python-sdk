# ForecastRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**forecast_period** | **int** | Number of future periods that should be forecasted | 
**confidence_level** | **float** | Confidence interval boundary value. | [optional]  if omitted the server will use the default value of 0.95
**seasonal** | **bool** | Whether the input data is seasonal | [optional]  if omitted the server will use the default value of False
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


