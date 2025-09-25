# JsonApiColorPalettePatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiColorPalettePatch**](JsonApiColorPalettePatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_color_palette_patch_document import JsonApiColorPalettePatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiColorPalettePatchDocument from a JSON string
json_api_color_palette_patch_document_instance = JsonApiColorPalettePatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiColorPalettePatchDocument.to_json())

# convert the object into a dict
json_api_color_palette_patch_document_dict = json_api_color_palette_patch_document_instance.to_dict()
# create an instance of JsonApiColorPalettePatchDocument from a dict
json_api_color_palette_patch_document_from_dict = JsonApiColorPalettePatchDocument.from_dict(json_api_color_palette_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


