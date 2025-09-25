# JsonApiColorPaletteOut

JSON:API representation of colorPalette entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiColorPaletteInAttributes**](JsonApiColorPaletteInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_color_palette_out import JsonApiColorPaletteOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiColorPaletteOut from a JSON string
json_api_color_palette_out_instance = JsonApiColorPaletteOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiColorPaletteOut.to_json())

# convert the object into a dict
json_api_color_palette_out_dict = json_api_color_palette_out_instance.to_dict()
# create an instance of JsonApiColorPaletteOut from a dict
json_api_color_palette_out_from_dict = JsonApiColorPaletteOut.from_dict(json_api_color_palette_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


