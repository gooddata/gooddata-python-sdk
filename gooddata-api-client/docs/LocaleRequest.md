# LocaleRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**locale** | **str** | Requested locale in the form of language tag (see RFC 5646). | 

## Example

```python
from gooddata_api_client.models.locale_request import LocaleRequest

# TODO update the JSON string below
json = "{}"
# create an instance of LocaleRequest from a JSON string
locale_request_instance = LocaleRequest.from_json(json)
# print the JSON string representation of the object
print(LocaleRequest.to_json())

# convert the object into a dict
locale_request_dict = locale_request_instance.to_dict()
# create an instance of LocaleRequest from a dict
locale_request_from_dict = LocaleRequest.from_dict(locale_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


