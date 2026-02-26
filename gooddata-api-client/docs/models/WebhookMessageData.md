# gooddata_api_client.model.webhook_message_data.WebhookMessageData

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**automation** | [**WebhookAutomationInfo**](WebhookAutomationInfo.md) | [**WebhookAutomationInfo**](WebhookAutomationInfo.md) |  | 
**alert** | [**AlertDescription**](AlertDescription.md) | [**AlertDescription**](AlertDescription.md) |  | [optional] 
**[dashboardTabularExports](#dashboardTabularExports)** | list, tuple,  | tuple,  |  | [optional] 
**[details](#details)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | [optional] 
**[filters](#filters)** | list, tuple,  | tuple,  |  | [optional] 
**[imageExports](#imageExports)** | list, tuple,  | tuple,  |  | [optional] 
**notificationSource** | str,  | str,  |  | [optional] 
**[rawExports](#rawExports)** | list, tuple,  | tuple,  |  | [optional] 
**[recipients](#recipients)** | list, tuple,  | tuple,  |  | [optional] 
**remainingActionCount** | decimal.Decimal, int,  | decimal.Decimal,  |  | [optional] value must be a 32 bit integer
**[slidesExports](#slidesExports)** | list, tuple,  | tuple,  |  | [optional] 
**[tabularExports](#tabularExports)** | list, tuple,  | tuple,  |  | [optional] 
**[visualExports](#visualExports)** | list, tuple,  | tuple,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# dashboardTabularExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) |  | 

# details

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type | [optional] 

# filters

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**NotificationFilter**](NotificationFilter.md) | [**NotificationFilter**](NotificationFilter.md) | [**NotificationFilter**](NotificationFilter.md) |  | 

# imageExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) |  | 

# rawExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) |  | 

# recipients

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**WebhookRecipient**](WebhookRecipient.md) | [**WebhookRecipient**](WebhookRecipient.md) | [**WebhookRecipient**](WebhookRecipient.md) |  | 

# slidesExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) |  | 

# tabularExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) |  | 

# visualExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) | [**ExportResult**](ExportResult.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

