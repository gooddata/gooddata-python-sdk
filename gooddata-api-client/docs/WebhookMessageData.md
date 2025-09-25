# WebhookMessageData


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alert** | [**AlertDescription**](AlertDescription.md) |  | [optional] 
**automation** | [**WebhookAutomationInfo**](WebhookAutomationInfo.md) |  | 
**dashboard_tabular_exports** | [**List[ExportResult]**](ExportResult.md) |  | [optional] 
**details** | **Dict[str, str]** |  | [optional] 
**filters** | [**List[NotificationFilter]**](NotificationFilter.md) |  | [optional] 
**image_exports** | [**List[ExportResult]**](ExportResult.md) |  | [optional] 
**notification_source** | **str** |  | [optional] 
**raw_exports** | [**List[ExportResult]**](ExportResult.md) |  | [optional] 
**recipients** | [**List[WebhookRecipient]**](WebhookRecipient.md) |  | [optional] 
**remaining_action_count** | **int** |  | [optional] 
**slides_exports** | [**List[ExportResult]**](ExportResult.md) |  | [optional] 
**tabular_exports** | [**List[ExportResult]**](ExportResult.md) |  | [optional] 
**visual_exports** | [**List[ExportResult]**](ExportResult.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.webhook_message_data import WebhookMessageData

# TODO update the JSON string below
json = "{}"
# create an instance of WebhookMessageData from a JSON string
webhook_message_data_instance = WebhookMessageData.from_json(json)
# print the JSON string representation of the object
print(WebhookMessageData.to_json())

# convert the object into a dict
webhook_message_data_dict = webhook_message_data_instance.to_dict()
# create an instance of WebhookMessageData from a dict
webhook_message_data_from_dict = WebhookMessageData.from_dict(webhook_message_data_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


