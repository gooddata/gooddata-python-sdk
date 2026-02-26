# gooddata_api_client.model.test_destination_request.TestDestinationRequest

Request body with notification channel destination to test.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Request body with notification channel destination to test. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[destination](#destination)** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 
**[externalRecipients](#externalRecipients)** | list, tuple, None,  | tuple, NoneClass,  | External recipients of the test result. | [optional] 
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

# externalRecipients

External recipients of the test result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  | External recipients of the test result. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AutomationExternalRecipient**](AutomationExternalRecipient.md) | [**AutomationExternalRecipient**](AutomationExternalRecipient.md) | [**AutomationExternalRecipient**](AutomationExternalRecipient.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

