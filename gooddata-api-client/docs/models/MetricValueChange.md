# gooddata_api_client.model.metric_value_change.MetricValueChange

Individual change analysis data item

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Individual change analysis data item | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**overallMetricValueInReferencePeriod** | decimal.Decimal, int, float,  | decimal.Decimal,  | The overall metric value in the reference period | value must be a 64 bit float
**metricValueDeltaAbs** | decimal.Decimal, int, float,  | decimal.Decimal,  | The absolute delta between analyzed and reference periods | value must be a 64 bit float
**isSignificantChange** | bool,  | BoolClass,  | Whether the change is statistically significant | 
**attributeValue** | str,  | str,  | The value of the attribute being analyzed | 
**attributeValuesChangeStd** | decimal.Decimal, int, float,  | decimal.Decimal,  | The standard deviation of attribute value changes for the attribute being analyzed | value must be a 64 bit float
**attributeName** | str,  | str,  | The name of the attribute being analyzed | 
**metricValueInAnalyzedPeriod** | decimal.Decimal, int, float,  | decimal.Decimal,  | The metric value in the analyzed period | value must be a 64 bit float
**metricValueDelta** | decimal.Decimal, int, float,  | decimal.Decimal,  | The delta between analyzed and reference periods | value must be a 64 bit float
**metricValueInReferencePeriod** | decimal.Decimal, int, float,  | decimal.Decimal,  | The metric value in the reference period | value must be a 64 bit float
**attributeValuesChangeMean** | decimal.Decimal, int, float,  | decimal.Decimal,  | The mean of attribute value changes for the attribute being analyzed | value must be a 64 bit float
**overallMetricValueInAnalyzedPeriod** | decimal.Decimal, int, float,  | decimal.Decimal,  | The overall metric value in the analyzed period | value must be a 64 bit float
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

