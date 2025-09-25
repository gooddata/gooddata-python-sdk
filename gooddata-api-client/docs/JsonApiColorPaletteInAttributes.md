# JsonApiColorPaletteInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON content. Maximum supported length is 15000 characters. | 
**name** | **str** |  | 

## Example

```python
from gooddata_api_client.models.json_api_color_palette_in_attributes import JsonApiColorPaletteInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiColorPaletteInAttributes from a JSON string
json_api_color_palette_in_attributes_instance = JsonApiColorPaletteInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiColorPaletteInAttributes.to_json())

# convert the object into a dict
json_api_color_palette_in_attributes_dict = json_api_color_palette_in_attributes_instance.to_dict()
# create an instance of JsonApiColorPaletteInAttributes from a dict
json_api_color_palette_in_attributes_from_dict = JsonApiColorPaletteInAttributes.from_dict(json_api_color_palette_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


