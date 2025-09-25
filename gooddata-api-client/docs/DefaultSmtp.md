# DefaultSmtp

Default SMTP destination for notifications.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_email** | **str** | E-mail address to send notifications from. Currently this does not have any effect. E-mail &#39;no-reply@gooddata.com&#39; is used instead. | [optional] [default to 'no-reply@gooddata.com']
**from_email_name** | **str** | An optional e-mail name to send notifications from. Currently this does not have any effect. E-mail from name &#39;GoodData&#39; is used instead. | [optional] [default to 'GoodData']
**type** | **str** | The destination type. | 

## Example

```python
from gooddata_api_client.models.default_smtp import DefaultSmtp

# TODO update the JSON string below
json = "{}"
# create an instance of DefaultSmtp from a JSON string
default_smtp_instance = DefaultSmtp.from_json(json)
# print the JSON string representation of the object
print(DefaultSmtp.to_json())

# convert the object into a dict
default_smtp_dict = default_smtp_instance.to_dict()
# create an instance of DefaultSmtp from a dict
default_smtp_from_dict = DefaultSmtp.from_dict(default_smtp_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


