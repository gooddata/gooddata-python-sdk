# JsonApiJwkOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiJwkOut**](JsonApiJwkOut.md) |  | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_jwk_out_document import JsonApiJwkOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiJwkOutDocument from a JSON string
json_api_jwk_out_document_instance = JsonApiJwkOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiJwkOutDocument.to_json())

# convert the object into a dict
json_api_jwk_out_document_dict = json_api_jwk_out_document_instance.to_dict()
# create an instance of JsonApiJwkOutDocument from a dict
json_api_jwk_out_document_from_dict = JsonApiJwkOutDocument.from_dict(json_api_jwk_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


