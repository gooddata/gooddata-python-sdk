# AutomationAlert


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**condition** | [**AutomationAlertCondition**](AutomationAlertCondition.md) |  | 
**execution** | [**AlertAfm**](AlertAfm.md) |  | 
**trigger** | **str** | Trigger behavior for the alert. ALWAYS - alert is triggered every time the condition is met. ONCE - alert is triggered only once when the condition is met.  | [optional] [default to 'ALWAYS']

## Example

```python
from gooddata_api_client.models.automation_alert import AutomationAlert

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationAlert from a JSON string
automation_alert_instance = AutomationAlert.from_json(json)
# print the JSON string representation of the object
print(AutomationAlert.to_json())

# convert the object into a dict
automation_alert_dict = automation_alert_instance.to_dict()
# create an instance of AutomationAlert from a dict
automation_alert_from_dict = AutomationAlert.from_dict(automation_alert_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


