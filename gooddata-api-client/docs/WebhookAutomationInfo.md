# WebhookAutomationInfo


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_title** | **str** |  | [optional] 
**dashboard_url** | **str** |  | 
**id** | **str** |  | 
**is_custom_dashboard_url** | **bool** |  | 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.webhook_automation_info import WebhookAutomationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookAutomationInfo from a JSON string
webhook_automation_info_instance = WebhookAutomationInfo.from_json(json)
# print the JSON string representation of the object
print(WebhookAutomationInfo.to_json())

# convert the object into a dict
webhook_automation_info_dict = webhook_automation_info_instance.to_dict()
# create an instance of WebhookAutomationInfo from a dict
webhook_automation_info_from_dict = WebhookAutomationInfo.from_dict(webhook_automation_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


