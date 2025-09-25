# JsonApiOrganizationSettingInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON content. Maximum supported length is 15000 characters. | [optional] 
**type** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_setting_in_attributes import JsonApiOrganizationSettingInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationSettingInAttributes from a JSON string
json_api_organization_setting_in_attributes_instance = JsonApiOrganizationSettingInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationSettingInAttributes.to_json())

# convert the object into a dict
json_api_organization_setting_in_attributes_dict = json_api_organization_setting_in_attributes_instance.to_dict()
# create an instance of JsonApiOrganizationSettingInAttributes from a dict
json_api_organization_setting_in_attributes_from_dict = JsonApiOrganizationSettingInAttributes.from_dict(json_api_organization_setting_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


