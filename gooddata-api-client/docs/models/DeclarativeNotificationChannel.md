# gooddata_api_client.model.declarative_notification_channel.DeclarativeNotificationChannel

A declarative form of a particular notification channel.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | A declarative form of a particular notification channel. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Identifier of a notification channel | 
**allowedRecipients** | str,  | str,  | Allowed recipients of notifications from this channel. CREATOR - only the creator INTERNAL - all users within the organization EXTERNAL - all recipients including those outside the organization  | [optional] must be one of ["CREATOR", "INTERNAL", "EXTERNAL", ] if omitted the server will use the default value of "INTERNAL"
**customDashboardUrl** | str,  | str,  | Custom dashboard url that is going to be used in the notification. If not specified it is going to be deduced based on the context. Allowed placeholders are: {workspaceId} {dashboardId} {automationId} {asOfDate}  | [optional] 
**dashboardLinkVisibility** | str,  | str,  | Dashboard link visibility in notifications. HIDDEN - the link will not be included INTERNAL_ONLY - only internal users will see the link ALL - all users will see the link  | [optional] must be one of ["HIDDEN", "INTERNAL_ONLY", "ALL", ] if omitted the server will use the default value of "INTERNAL_ONLY"
**description** | str,  | str,  | Description of a notification channel. | [optional] 
**[destination](#destination)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | [optional] 
**destinationType** | None, str,  | NoneClass, str,  |  | [optional] must be one of ["WEBHOOK", "SMTP", "DEFAULT_SMTP", "IN_PLATFORM", ] 
**inPlatformNotification** | str,  | str,  | In-platform notifications configuration. No effect if the destination type is IN_PLATFORM. DISABLED - in-platform notifications are not sent ENABLED - in-platform notifications are sent in addition to the regular notifications  | [optional] must be one of ["DISABLED", "ENABLED", ] if omitted the server will use the default value of "DISABLED"
**name** | str,  | str,  | Name of a notification channel. | [optional] 
**notificationSource** | str,  | str,  | Human-readable description of the source of the notification. If specified, this propertywill be included in the notifications to this channel.Allowed placeholders are: {{workspaceId}} {{workspaceName}} {{workspaceDescription}} {{dashboardId}} {{dashboardName}} {{dashboardDescription}}  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# destination

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[DefaultSmtp](DefaultSmtp.md) | [**DefaultSmtp**](DefaultSmtp.md) | [**DefaultSmtp**](DefaultSmtp.md) |  | 
[InPlatform](InPlatform.md) | [**InPlatform**](InPlatform.md) | [**InPlatform**](InPlatform.md) |  | 
[Smtp](Smtp.md) | [**Smtp**](Smtp.md) | [**Smtp**](Smtp.md) |  | 
[Webhook](Webhook.md) | [**Webhook**](Webhook.md) | [**Webhook**](Webhook.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

