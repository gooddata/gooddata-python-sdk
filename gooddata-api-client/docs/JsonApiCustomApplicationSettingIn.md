# JsonApiCustomApplicationSettingIn

JSON:API representation of customApplicationSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiCustomApplicationSettingInAttributes**](JsonApiCustomApplicationSettingInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_custom_application_setting_in import JsonApiCustomApplicationSettingIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCustomApplicationSettingIn from a JSON string
json_api_custom_application_setting_in_instance = JsonApiCustomApplicationSettingIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiCustomApplicationSettingIn.to_json())

# convert the object into a dict
json_api_custom_application_setting_in_dict = json_api_custom_application_setting_in_instance.to_dict()
# create an instance of JsonApiCustomApplicationSettingIn from a dict
json_api_custom_application_setting_in_from_dict = JsonApiCustomApplicationSettingIn.from_dict(json_api_custom_application_setting_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


