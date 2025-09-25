# AutomationNotification


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**WebhookMessage**](WebhookMessage.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_notification import AutomationNotification

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationNotification from a JSON string
automation_notification_instance = AutomationNotification.from_json(json)
# print the JSON string representation of the object
print(AutomationNotification.to_json())

# convert the object into a dict
automation_notification_dict = automation_notification_instance.to_dict()
# create an instance of AutomationNotification from a dict
automation_notification_from_dict = AutomationNotification.from_dict(automation_notification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


