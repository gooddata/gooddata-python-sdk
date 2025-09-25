# JsonApiOrganizationOutAttributesCacheSettings


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cache_strategy** | **str** |  | [optional] 
**extra_cache_budget** | **int** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_out_attributes_cache_settings import JsonApiOrganizationOutAttributesCacheSettings

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationOutAttributesCacheSettings from a JSON string
json_api_organization_out_attributes_cache_settings_instance = JsonApiOrganizationOutAttributesCacheSettings.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationOutAttributesCacheSettings.to_json())

# convert the object into a dict
json_api_organization_out_attributes_cache_settings_dict = json_api_organization_out_attributes_cache_settings_instance.to_dict()
# create an instance of JsonApiOrganizationOutAttributesCacheSettings from a dict
json_api_organization_out_attributes_cache_settings_from_dict = JsonApiOrganizationOutAttributesCacheSettings.from_dict(json_api_organization_out_attributes_cache_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


