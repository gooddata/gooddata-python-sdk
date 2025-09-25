# JsonApiColorPaletteIn

JSON:API representation of colorPalette entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiColorPaletteInAttributes**](JsonApiColorPaletteInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_color_palette_in import JsonApiColorPaletteIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiColorPaletteIn from a JSON string
json_api_color_palette_in_instance = JsonApiColorPaletteIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiColorPaletteIn.to_json())

# convert the object into a dict
json_api_color_palette_in_dict = json_api_color_palette_in_instance.to_dict()
# create an instance of JsonApiColorPaletteIn from a dict
json_api_color_palette_in_from_dict = JsonApiColorPaletteIn.from_dict(json_api_color_palette_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


