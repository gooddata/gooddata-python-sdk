# JsonApiFilterViewPatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiFilterViewPatch**](JsonApiFilterViewPatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_filter_view_patch_document import JsonApiFilterViewPatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFilterViewPatchDocument from a JSON string
json_api_filter_view_patch_document_instance = JsonApiFilterViewPatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiFilterViewPatchDocument.to_json())

# convert the object into a dict
json_api_filter_view_patch_document_dict = json_api_filter_view_patch_document_instance.to_dict()
# create an instance of JsonApiFilterViewPatchDocument from a dict
json_api_filter_view_patch_document_from_dict = JsonApiFilterViewPatchDocument.from_dict(json_api_filter_view_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


