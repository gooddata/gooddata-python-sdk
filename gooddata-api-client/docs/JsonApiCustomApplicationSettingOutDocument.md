# JsonApiCustomApplicationSettingOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiCustomApplicationSettingOut**](JsonApiCustomApplicationSettingOut.md) |  | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_custom_application_setting_out_document import JsonApiCustomApplicationSettingOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCustomApplicationSettingOutDocument from a JSON string
json_api_custom_application_setting_out_document_instance = JsonApiCustomApplicationSettingOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiCustomApplicationSettingOutDocument.to_json())

# convert the object into a dict
json_api_custom_application_setting_out_document_dict = json_api_custom_application_setting_out_document_instance.to_dict()
# create an instance of JsonApiCustomApplicationSettingOutDocument from a dict
json_api_custom_application_setting_out_document_from_dict = JsonApiCustomApplicationSettingOutDocument.from_dict(json_api_custom_application_setting_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


