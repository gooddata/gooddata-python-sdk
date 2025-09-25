# TriggerAutomationRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**automation** | [**AdHocAutomation**](AdHocAutomation.md) |  | 

## Example

```python
from gooddata_api_client.models.trigger_automation_request import TriggerAutomationRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TriggerAutomationRequest from a JSON string
trigger_automation_request_instance = TriggerAutomationRequest.from_json(json)
# print the JSON string representation of the object
print(TriggerAutomationRequest.to_json())

# convert the object into a dict
trigger_automation_request_dict = trigger_automation_request_instance.to_dict()
# create an instance of TriggerAutomationRequest from a dict
trigger_automation_request_from_dict = TriggerAutomationRequest.from_dict(trigger_automation_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


