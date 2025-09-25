# JsonApiCspDirectiveOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiCspDirectiveOut**](JsonApiCspDirectiveOut.md) |  | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_csp_directive_out_document import JsonApiCspDirectiveOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCspDirectiveOutDocument from a JSON string
json_api_csp_directive_out_document_instance = JsonApiCspDirectiveOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiCspDirectiveOutDocument.to_json())

# convert the object into a dict
json_api_csp_directive_out_document_dict = json_api_csp_directive_out_document_instance.to_dict()
# create an instance of JsonApiCspDirectiveOutDocument from a dict
json_api_csp_directive_out_document_from_dict = JsonApiCspDirectiveOutDocument.from_dict(json_api_csp_directive_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


