# gooddata_api_client.model.ad_hoc_automation.AdHocAutomation

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**alert** | [**AutomationAlert**](AutomationAlert.md) | [**AutomationAlert**](AutomationAlert.md) |  | [optional] 
**analyticalDashboard** | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) |  | [optional] 
**[dashboardTabularExports](#dashboardTabularExports)** | list, tuple,  | tuple,  |  | [optional] 
**description** | str,  | str,  |  | [optional] 
**[details](#details)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Additional details to be included in the automated message. | [optional] 
**[externalRecipients](#externalRecipients)** | list, tuple,  | tuple,  | External recipients of the automation action results. | [optional] 
**[imageExports](#imageExports)** | list, tuple,  | tuple,  |  | [optional] 
**metadata** | [**AutomationMetadata**](AutomationMetadata.md) | [**AutomationMetadata**](AutomationMetadata.md) |  | [optional] 
**notificationChannel** | [**DeclarativeNotificationChannelIdentifier**](DeclarativeNotificationChannelIdentifier.md) | [**DeclarativeNotificationChannelIdentifier**](DeclarativeNotificationChannelIdentifier.md) |  | [optional] 
**[rawExports](#rawExports)** | list, tuple,  | tuple,  |  | [optional] 
**[recipients](#recipients)** | list, tuple,  | tuple,  |  | [optional] 
**[slidesExports](#slidesExports)** | list, tuple,  | tuple,  |  | [optional] 
**[tabularExports](#tabularExports)** | list, tuple,  | tuple,  |  | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | A list of tags. | [optional] 
**title** | str,  | str,  |  | [optional] 
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
[**AutomationDashboardTabularExport**](AutomationDashboardTabularExport.md) | [**AutomationDashboardTabularExport**](AutomationDashboardTabularExport.md) | [**AutomationDashboardTabularExport**](AutomationDashboardTabularExport.md) |  | 

# details

Additional details to be included in the automated message.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Additional details to be included in the automated message. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type Additional details to be included in the automated message. | [optional] 

# externalRecipients

External recipients of the automation action results.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | External recipients of the automation action results. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AutomationExternalRecipient**](AutomationExternalRecipient.md) | [**AutomationExternalRecipient**](AutomationExternalRecipient.md) | [**AutomationExternalRecipient**](AutomationExternalRecipient.md) |  | 

# imageExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AutomationImageExport**](AutomationImageExport.md) | [**AutomationImageExport**](AutomationImageExport.md) | [**AutomationImageExport**](AutomationImageExport.md) |  | 

# rawExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AutomationRawExport**](AutomationRawExport.md) | [**AutomationRawExport**](AutomationRawExport.md) | [**AutomationRawExport**](AutomationRawExport.md) |  | 

# recipients

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | 

# slidesExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AutomationSlidesExport**](AutomationSlidesExport.md) | [**AutomationSlidesExport**](AutomationSlidesExport.md) | [**AutomationSlidesExport**](AutomationSlidesExport.md) |  | 

# tabularExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AutomationTabularExport**](AutomationTabularExport.md) | [**AutomationTabularExport**](AutomationTabularExport.md) | [**AutomationTabularExport**](AutomationTabularExport.md) |  | 

# tags

A list of tags.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of tags. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# visualExports

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AutomationVisualExport**](AutomationVisualExport.md) | [**AutomationVisualExport**](AutomationVisualExport.md) | [**AutomationVisualExport**](AutomationVisualExport.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

