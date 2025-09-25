# AutomationAlertCondition


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comparison** | [**Comparison**](Comparison.md) |  | 
**range** | [**Range**](Range.md) |  | 
**relative** | [**Relative**](Relative.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_alert_condition import AutomationAlertCondition

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationAlertCondition from a JSON string
automation_alert_condition_instance = AutomationAlertCondition.from_json(json)
# print the JSON string representation of the object
print(AutomationAlertCondition.to_json())

# convert the object into a dict
automation_alert_condition_dict = automation_alert_condition_instance.to_dict()
# create an instance of AutomationAlertCondition from a dict
automation_alert_condition_from_dict = AutomationAlertCondition.from_dict(automation_alert_condition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


