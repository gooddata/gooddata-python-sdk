# JsonApiCspDirectivePatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiCspDirectivePatch**](JsonApiCspDirectivePatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_csp_directive_patch_document import JsonApiCspDirectivePatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCspDirectivePatchDocument from a JSON string
json_api_csp_directive_patch_document_instance = JsonApiCspDirectivePatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiCspDirectivePatchDocument.to_json())

# convert the object into a dict
json_api_csp_directive_patch_document_dict = json_api_csp_directive_patch_document_instance.to_dict()
# create an instance of JsonApiCspDirectivePatchDocument from a dict
json_api_csp_directive_patch_document_from_dict = JsonApiCspDirectivePatchDocument.from_dict(json_api_csp_directive_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


