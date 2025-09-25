# JsonApiIdentityProviderInDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiIdentityProviderIn**](JsonApiIdentityProviderIn.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_identity_provider_in_document import JsonApiIdentityProviderInDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiIdentityProviderInDocument from a JSON string
json_api_identity_provider_in_document_instance = JsonApiIdentityProviderInDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiIdentityProviderInDocument.to_json())

# convert the object into a dict
json_api_identity_provider_in_document_dict = json_api_identity_provider_in_document_instance.to_dict()
# create an instance of JsonApiIdentityProviderInDocument from a dict
json_api_identity_provider_in_document_from_dict = JsonApiIdentityProviderInDocument.from_dict(json_api_identity_provider_in_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


