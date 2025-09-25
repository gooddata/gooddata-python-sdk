# Smtp

Custom SMTP destination for notifications. The properties host, port, username, and password are required on create and update

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**from_email** | **str** | E-mail address to send notifications from. | [optional] [default to 'no-reply@gooddata.com']
**from_email_name** | **str** | An optional e-mail name to send notifications from. | [optional] [default to 'GoodData']
**host** | **str** | The SMTP server address. | [optional] 
**password** | **str** | The SMTP server password. | [optional] 
**port** | **int** | The SMTP server port. | [optional] 
**type** | **str** | The destination type. | 
**username** | **str** | The SMTP server username. | [optional] 

## Example

```python
from gooddata_api_client.models.smtp import Smtp

# TODO update the JSON string below
json = "{}"
# create an instance of Smtp from a JSON string
smtp_instance = Smtp.from_json(json)
# print the JSON string representation of the object
print(Smtp.to_json())

# convert the object into a dict
smtp_dict = smtp_instance.to_dict()
# create an instance of Smtp from a dict
smtp_from_dict = Smtp.from_dict(smtp_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


