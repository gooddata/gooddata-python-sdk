# JsonApiNotificationChannelIdentifierOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_recipients** | **str** | Allowed recipients of notifications from this channel. CREATOR - only the creator INTERNAL - all users within the organization EXTERNAL - all recipients including those outside the organization  | [optional] 
**description** | **str** |  | [optional] 
**destination_type** | **str** |  | [optional] 
**name** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_identifier_out_attributes import JsonApiNotificationChannelIdentifierOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelIdentifierOutAttributes from a JSON string
json_api_notification_channel_identifier_out_attributes_instance = JsonApiNotificationChannelIdentifierOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelIdentifierOutAttributes.to_json())

# convert the object into a dict
json_api_notification_channel_identifier_out_attributes_dict = json_api_notification_channel_identifier_out_attributes_instance.to_dict()
# create an instance of JsonApiNotificationChannelIdentifierOutAttributes from a dict
json_api_notification_channel_identifier_out_attributes_from_dict = JsonApiNotificationChannelIdentifierOutAttributes.from_dict(json_api_notification_channel_identifier_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


