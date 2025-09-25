# JsonApiNotificationChannelIdentifierOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiNotificationChannelIdentifierOutAttributes**](JsonApiNotificationChannelIdentifierOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_notification_channel_identifier_out_with_links import JsonApiNotificationChannelIdentifierOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiNotificationChannelIdentifierOutWithLinks from a JSON string
json_api_notification_channel_identifier_out_with_links_instance = JsonApiNotificationChannelIdentifierOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiNotificationChannelIdentifierOutWithLinks.to_json())

# convert the object into a dict
json_api_notification_channel_identifier_out_with_links_dict = json_api_notification_channel_identifier_out_with_links_instance.to_dict()
# create an instance of JsonApiNotificationChannelIdentifierOutWithLinks from a dict
json_api_notification_channel_identifier_out_with_links_from_dict = JsonApiNotificationChannelIdentifierOutWithLinks.from_dict(json_api_notification_channel_identifier_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


