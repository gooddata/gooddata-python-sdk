# JsonApiThemeOut

JSON:API representation of theme entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiColorPaletteInAttributes**](JsonApiColorPaletteInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_theme_out import JsonApiThemeOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiThemeOut from a JSON string
json_api_theme_out_instance = JsonApiThemeOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiThemeOut.to_json())

# convert the object into a dict
json_api_theme_out_dict = json_api_theme_out_instance.to_dict()
# create an instance of JsonApiThemeOut from a dict
json_api_theme_out_from_dict = JsonApiThemeOut.from_dict(json_api_theme_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


