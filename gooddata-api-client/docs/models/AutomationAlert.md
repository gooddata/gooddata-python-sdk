# gooddata_api_client.model.automation_alert.AutomationAlert

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**execution** | [**AlertAfm**](AlertAfm.md) | [**AlertAfm**](AlertAfm.md) |  | 
**[condition](#condition)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 
**interval** | str,  | str,  | Date granularity for the interval of ONCE_PER_INTERVAL trigger. Supported granularities: DAY, WEEK, MONTH, QUARTER, YEAR. | [optional] must be one of ["DAY", "WEEK", "MONTH", "QUARTER", "YEAR", ] 
**trigger** | str,  | str,  | Trigger behavior for the alert. ALWAYS - alert is triggered every time the condition is met. ONCE - alert is triggered only once when the condition is met. ONCE_PER_INTERVAL - alert is triggered when the condition is met, then suppressed for the interval. If no interval is specified, it behaves as ALWAYS.  | [optional] must be one of ["ALWAYS", "ONCE", "ONCE_PER_INTERVAL", ] if omitted the server will use the default value of "ALWAYS"
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# condition

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AnomalyDetectionWrapper](AnomalyDetectionWrapper.md) | [**AnomalyDetectionWrapper**](AnomalyDetectionWrapper.md) | [**AnomalyDetectionWrapper**](AnomalyDetectionWrapper.md) |  | 
[ComparisonWrapper](ComparisonWrapper.md) | [**ComparisonWrapper**](ComparisonWrapper.md) | [**ComparisonWrapper**](ComparisonWrapper.md) |  | 
[RangeWrapper](RangeWrapper.md) | [**RangeWrapper**](RangeWrapper.md) | [**RangeWrapper**](RangeWrapper.md) |  | 
[RelativeWrapper](RelativeWrapper.md) | [**RelativeWrapper**](RelativeWrapper.md) | [**RelativeWrapper**](RelativeWrapper.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

