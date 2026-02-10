# AutomationAlert


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition** | [**AutomationAlertCondition**](AutomationAlertCondition.md) |  | 
**execution** | [**AlertAfm**](AlertAfm.md) |  | 
**interval** | **str** | Date granularity for the interval of ONCE_PER_INTERVAL trigger. Supported granularities: DAY, WEEK, MONTH, QUARTER, YEAR. | [optional] 
**trigger** | **str** | Trigger behavior for the alert. ALWAYS - alert is triggered every time the condition is met. ONCE - alert is triggered only once when the condition is met. ONCE_PER_INTERVAL - alert is triggered when the condition is met, then suppressed for the interval. If no interval is specified, it behaves as ALWAYS.  | [optional]  if omitted the server will use the default value of "ALWAYS"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


