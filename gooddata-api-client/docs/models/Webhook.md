# gooddata_api_client.model.webhook.Webhook

Webhook destination for notifications. The property url is required on create and update.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Webhook destination for notifications. The property url is required on create and update. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**type** | str,  | str,  | The destination type. | must be one of ["WEBHOOK", ] 
**hasSecretKey** | None, bool,  | NoneClass, BoolClass,  | Flag indicating if webhook has a hmac secret key. | [optional] 
**hasToken** | None, bool,  | NoneClass, BoolClass,  | Flag indicating if webhook has a token. | [optional] 
**secretKey** | None, str,  | NoneClass, str,  | Hmac secret key for the webhook signature. | [optional] 
**token** | None, str,  | NoneClass, str,  | Bearer token for the webhook. | [optional] 
**url** | str,  | str,  | The webhook URL. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

### Composed Schemas (allOf/anyOf/oneOf/not)
#### allOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[all_of_0](#all_of_0) | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

# all_of_0

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**hasSecretKey** | None, bool,  | NoneClass, BoolClass,  | Flag indicating if webhook has a hmac secret key. | [optional] 
**hasToken** | None, bool,  | NoneClass, BoolClass,  | Flag indicating if webhook has a token. | [optional] 
**secretKey** | None, str,  | NoneClass, str,  | Hmac secret key for the webhook signature. | [optional] 
**token** | None, str,  | NoneClass, str,  | Bearer token for the webhook. | [optional] 
**type** | str,  | str,  | The destination type. | [optional] must be one of ["WEBHOOK", ] 
**url** | str,  | str,  | The webhook URL. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

