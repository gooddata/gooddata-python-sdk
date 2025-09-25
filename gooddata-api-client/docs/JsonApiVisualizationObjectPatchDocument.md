# JsonApiVisualizationObjectPatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiVisualizationObjectPatch**](JsonApiVisualizationObjectPatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_visualization_object_patch_document import JsonApiVisualizationObjectPatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiVisualizationObjectPatchDocument from a JSON string
json_api_visualization_object_patch_document_instance = JsonApiVisualizationObjectPatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiVisualizationObjectPatchDocument.to_json())

# convert the object into a dict
json_api_visualization_object_patch_document_dict = json_api_visualization_object_patch_document_instance.to_dict()
# create an instance of JsonApiVisualizationObjectPatchDocument from a dict
json_api_visualization_object_patch_document_from_dict = JsonApiVisualizationObjectPatchDocument.from_dict(json_api_visualization_object_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


