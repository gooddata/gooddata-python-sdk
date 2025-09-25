# JsonApiOrganizationSettingIn

JSON:API representation of organizationSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationSettingInAttributes**](JsonApiOrganizationSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_organization_setting_in import JsonApiOrganizationSettingIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationSettingIn from a JSON string
json_api_organization_setting_in_instance = JsonApiOrganizationSettingIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationSettingIn.to_json())

# convert the object into a dict
json_api_organization_setting_in_dict = json_api_organization_setting_in_instance.to_dict()
# create an instance of JsonApiOrganizationSettingIn from a dict
json_api_organization_setting_in_from_dict = JsonApiOrganizationSettingIn.from_dict(json_api_organization_setting_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


