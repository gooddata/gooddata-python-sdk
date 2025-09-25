# JsonApiFilterContextPatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiFilterContextPatch**](JsonApiFilterContextPatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_filter_context_patch_document import JsonApiFilterContextPatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterContextPatchDocument from a JSON string
json_api_filter_context_patch_document_instance = JsonApiFilterContextPatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterContextPatchDocument.to_json())

# convert the object into a dict
json_api_filter_context_patch_document_dict = json_api_filter_context_patch_document_instance.to_dict()
# create an instance of JsonApiFilterContextPatchDocument from a dict
json_api_filter_context_patch_document_from_dict = JsonApiFilterContextPatchDocument.from_dict(json_api_filter_context_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


