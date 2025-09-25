# JsonApiCustomApplicationSettingPatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiCustomApplicationSettingPatch**](JsonApiCustomApplicationSettingPatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_custom_application_setting_patch_document import JsonApiCustomApplicationSettingPatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCustomApplicationSettingPatchDocument from a JSON string
json_api_custom_application_setting_patch_document_instance = JsonApiCustomApplicationSettingPatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiCustomApplicationSettingPatchDocument.to_json())

# convert the object into a dict
json_api_custom_application_setting_patch_document_dict = json_api_custom_application_setting_patch_document_instance.to_dict()
# create an instance of JsonApiCustomApplicationSettingPatchDocument from a dict
json_api_custom_application_setting_patch_document_from_dict = JsonApiCustomApplicationSettingPatchDocument.from_dict(json_api_custom_application_setting_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


