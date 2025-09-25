# JsonApiOrganizationSettingOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationSettingInAttributes**](JsonApiOrganizationSettingInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_setting_out_with_links import JsonApiOrganizationSettingOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationSettingOutWithLinks from a JSON string
json_api_organization_setting_out_with_links_instance = JsonApiOrganizationSettingOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationSettingOutWithLinks.to_json())

# convert the object into a dict
json_api_organization_setting_out_with_links_dict = json_api_organization_setting_out_with_links_instance.to_dict()
# create an instance of JsonApiOrganizationSettingOutWithLinks from a dict
json_api_organization_setting_out_with_links_from_dict = JsonApiOrganizationSettingOutWithLinks.from_dict(json_api_organization_setting_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


