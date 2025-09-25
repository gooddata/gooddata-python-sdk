# JsonApiCustomApplicationSettingPatchAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application_name** | **str** |  | [optional] 
**content** | **object** | Free-form JSON content. Maximum supported length is 15000 characters. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_custom_application_setting_patch_attributes import JsonApiCustomApplicationSettingPatchAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCustomApplicationSettingPatchAttributes from a JSON string
json_api_custom_application_setting_patch_attributes_instance = JsonApiCustomApplicationSettingPatchAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiCustomApplicationSettingPatchAttributes.to_json())

# convert the object into a dict
json_api_custom_application_setting_patch_attributes_dict = json_api_custom_application_setting_patch_attributes_instance.to_dict()
# create an instance of JsonApiCustomApplicationSettingPatchAttributes from a dict
json_api_custom_application_setting_patch_attributes_from_dict = JsonApiCustomApplicationSettingPatchAttributes.from_dict(json_api_custom_application_setting_patch_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


