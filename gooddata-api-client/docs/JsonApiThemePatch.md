# JsonApiThemePatch

JSON:API representation of patching theme entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiColorPalettePatchAttributes**](JsonApiColorPalettePatchAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_theme_patch import JsonApiThemePatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiThemePatch from a JSON string
json_api_theme_patch_instance = JsonApiThemePatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiThemePatch.to_json())

# convert the object into a dict
json_api_theme_patch_dict = json_api_theme_patch_instance.to_dict()
# create an instance of JsonApiThemePatch from a dict
json_api_theme_patch_from_dict = JsonApiThemePatch.from_dict(json_api_theme_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


