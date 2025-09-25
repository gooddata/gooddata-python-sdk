# JsonApiDataSourcePatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiDataSourcePatch**](JsonApiDataSourcePatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_data_source_patch_document import JsonApiDataSourcePatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourcePatchDocument from a JSON string
json_api_data_source_patch_document_instance = JsonApiDataSourcePatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourcePatchDocument.to_json())

# convert the object into a dict
json_api_data_source_patch_document_dict = json_api_data_source_patch_document_instance.to_dict()
# create an instance of JsonApiDataSourcePatchDocument from a dict
json_api_data_source_patch_document_from_dict = JsonApiDataSourcePatchDocument.from_dict(json_api_data_source_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


