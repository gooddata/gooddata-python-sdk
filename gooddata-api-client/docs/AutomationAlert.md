# AutomationAlert


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition** | [**AutomationAlertCondition**](AutomationAlertCondition.md) |  | 
**execution** | [**AlertAfm**](AlertAfm.md) |  | 
**trigger** | **str** | Trigger behavior for the alert. ALWAYS - alert is triggered every time the condition is met. ONCE - alert is triggered only once when the condition is met.  | [optional]  if omitted the server will use the default value of "ALWAYS"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


