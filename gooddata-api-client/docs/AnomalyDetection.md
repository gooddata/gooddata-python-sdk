# AnomalyDetection


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**granularity** | **str** | Date granularity for anomaly detection. Only time-based granularities are supported (HOUR, DAY, WEEK, MONTH, QUARTER, YEAR). | 
**measure** | [**LocalIdentifier**](LocalIdentifier.md) |  | 
**sensitivity** | **str** | Sensitivity level for anomaly detection | [optional]  if omitted the server will use the default value of "MEDIUM"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


