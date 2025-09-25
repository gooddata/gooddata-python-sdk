# JsonApiOrganizationSettingPatch

JSON:API representation of patching organizationSetting entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationSettingInAttributes**](JsonApiOrganizationSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_organization_setting_patch import JsonApiOrganizationSettingPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationSettingPatch from a JSON string
json_api_organization_setting_patch_instance = JsonApiOrganizationSettingPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationSettingPatch.to_json())

# convert the object into a dict
json_api_organization_setting_patch_dict = json_api_organization_setting_patch_instance.to_dict()
# create an instance of JsonApiOrganizationSettingPatch from a dict
json_api_organization_setting_patch_from_dict = JsonApiOrganizationSettingPatch.from_dict(json_api_organization_setting_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


