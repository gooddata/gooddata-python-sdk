# JsonApiOrganizationSettingOut

JSON:API representation of organizationSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationSettingInAttributes**](JsonApiOrganizationSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_organization_setting_out import JsonApiOrganizationSettingOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationSettingOut from a JSON string
json_api_organization_setting_out_instance = JsonApiOrganizationSettingOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationSettingOut.to_json())

# convert the object into a dict
json_api_organization_setting_out_dict = json_api_organization_setting_out_instance.to_dict()
# create an instance of JsonApiOrganizationSettingOut from a dict
json_api_organization_setting_out_from_dict = JsonApiOrganizationSettingOut.from_dict(json_api_organization_setting_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


