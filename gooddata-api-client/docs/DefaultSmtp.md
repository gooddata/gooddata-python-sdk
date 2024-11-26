# DefaultSmtp

Default SMTP destination for notifications.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | The destination type. | defaults to "DEFAULT_SMTP"
**from_email** | **str** | E-mail address to send notifications from. Currently this does not have any effect. E-mail &#39;no-reply@gooddata.com&#39; is used instead. | [optional]  if omitted the server will use the default value of no-reply@gooddata.com
**from_email_name** | **str** | An optional e-mail name to send notifications from. Currently this does not have any effect. E-mail from name &#39;GoodData&#39; is used instead. | [optional]  if omitted the server will use the default value of "GoodData"
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


