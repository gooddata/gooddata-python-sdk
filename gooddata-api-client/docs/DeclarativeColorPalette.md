# DeclarativeColorPalette

Color palette and its properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | 
**id** | **str** |  | 
**name** | **str** |  | 

## Example

```python
from gooddata_api_client.models.declarative_color_palette import DeclarativeColorPalette

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeColorPalette from a JSON string
declarative_color_palette_instance = DeclarativeColorPalette.from_json(json)
# print the JSON string representation of the object
print(DeclarativeColorPalette.to_json())

# convert the object into a dict
declarative_color_palette_dict = declarative_color_palette_instance.to_dict()
# create an instance of DeclarativeColorPalette from a dict
declarative_color_palette_from_dict = DeclarativeColorPalette.from_dict(declarative_color_palette_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


