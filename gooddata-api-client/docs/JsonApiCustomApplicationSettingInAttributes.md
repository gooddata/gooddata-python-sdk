# JsonApiCustomApplicationSettingInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application_name** | **str** |  | 
**content** | **object** | Free-form JSON content. Maximum supported length is 15000 characters. | 

## Example

```python
from gooddata_api_client.models.json_api_custom_application_setting_in_attributes import JsonApiCustomApplicationSettingInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCustomApplicationSettingInAttributes from a JSON string
json_api_custom_application_setting_in_attributes_instance = JsonApiCustomApplicationSettingInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiCustomApplicationSettingInAttributes.to_json())

# convert the object into a dict
json_api_custom_application_setting_in_attributes_dict = json_api_custom_application_setting_in_attributes_instance.to_dict()
# create an instance of JsonApiCustomApplicationSettingInAttributes from a dict
json_api_custom_application_setting_in_attributes_from_dict = JsonApiCustomApplicationSettingInAttributes.from_dict(json_api_custom_application_setting_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


