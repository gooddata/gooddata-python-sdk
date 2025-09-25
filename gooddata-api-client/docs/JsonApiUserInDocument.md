# JsonApiUserInDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiUserIn**](JsonApiUserIn.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_user_in_document import JsonApiUserInDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserInDocument from a JSON string
json_api_user_in_document_instance = JsonApiUserInDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserInDocument.to_json())

# convert the object into a dict
json_api_user_in_document_dict = json_api_user_in_document_instance.to_dict()
# create an instance of JsonApiUserInDocument from a dict
json_api_user_in_document_from_dict = JsonApiUserInDocument.from_dict(json_api_user_in_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


