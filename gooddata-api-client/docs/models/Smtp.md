# gooddata_api_client.model.smtp.Smtp

Custom SMTP destination for notifications. The properties host, port, username, and password are required on create and update

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom SMTP destination for notifications. The properties host, port, username, and password are required on create and update | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**type** | str,  | str,  | The destination type. | must be one of ["SMTP", ] 
**fromEmail** | str,  | str,  | E-mail address to send notifications from. | [optional] if omitted the server will use the default value of no-reply@gooddata.com
**fromEmailName** | str,  | str,  | An optional e-mail name to send notifications from. | [optional] if omitted the server will use the default value of "GoodData"
**host** | str,  | str,  | The SMTP server address. | [optional] 
**password** | str,  | str,  | The SMTP server password. | [optional] 
**port** | decimal.Decimal, int,  | decimal.Decimal,  | The SMTP server port. | [optional] must be one of [25, 465, 587, 2525, ] value must be a 32 bit integer
**username** | str,  | str,  | The SMTP server username. | [optional] 
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
**fromEmail** | str,  | str,  | E-mail address to send notifications from. | [optional] if omitted the server will use the default value of no-reply@gooddata.com
**fromEmailName** | str,  | str,  | An optional e-mail name to send notifications from. | [optional] if omitted the server will use the default value of "GoodData"
**host** | str,  | str,  | The SMTP server address. | [optional] 
**password** | str,  | str,  | The SMTP server password. | [optional] 
**port** | decimal.Decimal, int,  | decimal.Decimal,  | The SMTP server port. | [optional] must be one of [25, 465, 587, 2525, ] value must be a 32 bit integer
**type** | str,  | str,  | The destination type. | [optional] must be one of ["SMTP", ] 
**username** | str,  | str,  | The SMTP server username. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

