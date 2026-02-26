# gooddata_api_client.model.default_smtp.DefaultSmtp

Default SMTP destination for notifications.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Default SMTP destination for notifications. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**type** | str,  | str,  | The destination type. | must be one of ["DEFAULT_SMTP", ] 
**fromEmail** | str,  | str,  | E-mail address to send notifications from. Currently this does not have any effect. E-mail &#x27;no-reply@gooddata.com&#x27; is used instead. | [optional] if omitted the server will use the default value of no-reply@gooddata.com
**fromEmailName** | str,  | str,  | An optional e-mail name to send notifications from. Currently this does not have any effect. E-mail from name &#x27;GoodData&#x27; is used instead. | [optional] if omitted the server will use the default value of "GoodData"
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
**fromEmail** | str,  | str,  | E-mail address to send notifications from. Currently this does not have any effect. E-mail &#x27;no-reply@gooddata.com&#x27; is used instead. | [optional] if omitted the server will use the default value of no-reply@gooddata.com
**fromEmailName** | str,  | str,  | An optional e-mail name to send notifications from. Currently this does not have any effect. E-mail from name &#x27;GoodData&#x27; is used instead. | [optional] if omitted the server will use the default value of "GoodData"
**type** | str,  | str,  | The destination type. | [optional] must be one of ["DEFAULT_SMTP", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

