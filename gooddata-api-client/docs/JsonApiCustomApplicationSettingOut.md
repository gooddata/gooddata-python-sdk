# JsonApiCustomApplicationSettingOut

JSON:API representation of customApplicationSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiCustomApplicationSettingInAttributes**](JsonApiCustomApplicationSettingInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_custom_application_setting_out import JsonApiCustomApplicationSettingOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCustomApplicationSettingOut from a JSON string
json_api_custom_application_setting_out_instance = JsonApiCustomApplicationSettingOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiCustomApplicationSettingOut.to_json())

# convert the object into a dict
json_api_custom_application_setting_out_dict = json_api_custom_application_setting_out_instance.to_dict()
# create an instance of JsonApiCustomApplicationSettingOut from a dict
json_api_custom_application_setting_out_from_dict = JsonApiCustomApplicationSettingOut.from_dict(json_api_custom_application_setting_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


