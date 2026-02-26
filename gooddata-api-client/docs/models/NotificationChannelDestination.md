# gooddata_api_client.model.notification_channel_destination.NotificationChannelDestination

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**type** | str,  | str,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[Webhook](Webhook.md) | [**Webhook**](Webhook.md) | [**Webhook**](Webhook.md) |  | 
[Smtp](Smtp.md) | [**Smtp**](Smtp.md) | [**Smtp**](Smtp.md) |  | 
[DefaultSmtp](DefaultSmtp.md) | [**DefaultSmtp**](DefaultSmtp.md) | [**DefaultSmtp**](DefaultSmtp.md) |  | 
[InPlatform](InPlatform.md) | [**InPlatform**](InPlatform.md) | [**InPlatform**](InPlatform.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

