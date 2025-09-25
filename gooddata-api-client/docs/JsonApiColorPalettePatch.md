# JsonApiColorPalettePatch

JSON:API representation of patching colorPalette entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiColorPalettePatchAttributes**](JsonApiColorPalettePatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_color_palette_patch import JsonApiColorPalettePatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiColorPalettePatch from a JSON string
json_api_color_palette_patch_instance = JsonApiColorPalettePatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiColorPalettePatch.to_json())

# convert the object into a dict
json_api_color_palette_patch_dict = json_api_color_palette_patch_instance.to_dict()
# create an instance of JsonApiColorPalettePatch from a dict
json_api_color_palette_patch_from_dict = JsonApiColorPalettePatch.from_dict(json_api_color_palette_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


