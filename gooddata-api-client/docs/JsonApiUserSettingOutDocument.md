# JsonApiUserSettingOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiUserSettingOut**](JsonApiUserSettingOut.md) |  | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_setting_out_document import JsonApiUserSettingOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserSettingOutDocument from a JSON string
json_api_user_setting_out_document_instance = JsonApiUserSettingOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserSettingOutDocument.to_json())

# convert the object into a dict
json_api_user_setting_out_document_dict = json_api_user_setting_out_document_instance.to_dict()
# create an instance of JsonApiUserSettingOutDocument from a dict
json_api_user_setting_out_document_from_dict = JsonApiUserSettingOutDocument.from_dict(json_api_user_setting_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


