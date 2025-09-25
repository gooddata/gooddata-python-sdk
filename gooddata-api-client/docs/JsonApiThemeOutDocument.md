# JsonApiThemeOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiThemeOut**](JsonApiThemeOut.md) |  | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_theme_out_document import JsonApiThemeOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiThemeOutDocument from a JSON string
json_api_theme_out_document_instance = JsonApiThemeOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiThemeOutDocument.to_json())

# convert the object into a dict
json_api_theme_out_document_dict = json_api_theme_out_document_instance.to_dict()
# create an instance of JsonApiThemeOutDocument from a dict
json_api_theme_out_document_from_dict = JsonApiThemeOutDocument.from_dict(json_api_theme_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


