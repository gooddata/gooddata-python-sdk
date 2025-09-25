# AutomationExternalRecipient


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** | E-mail address to send notifications from. | 

## Example

```python
from gooddata_api_client.models.automation_external_recipient import AutomationExternalRecipient

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationExternalRecipient from a JSON string
automation_external_recipient_instance = AutomationExternalRecipient.from_json(json)
# print the JSON string representation of the object
print(AutomationExternalRecipient.to_json())

# convert the object into a dict
automation_external_recipient_dict = automation_external_recipient_instance.to_dict()
# create an instance of AutomationExternalRecipient from a dict
automation_external_recipient_from_dict = AutomationExternalRecipient.from_dict(automation_external_recipient_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


