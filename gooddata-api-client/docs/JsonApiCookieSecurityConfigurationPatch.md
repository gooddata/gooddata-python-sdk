# JsonApiCookieSecurityConfigurationPatch

JSON:API representation of patching cookieSecurityConfiguration entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiCookieSecurityConfigurationInAttributes**](JsonApiCookieSecurityConfigurationInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_cookie_security_configuration_patch import JsonApiCookieSecurityConfigurationPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCookieSecurityConfigurationPatch from a JSON string
json_api_cookie_security_configuration_patch_instance = JsonApiCookieSecurityConfigurationPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiCookieSecurityConfigurationPatch.to_json())

# convert the object into a dict
json_api_cookie_security_configuration_patch_dict = json_api_cookie_security_configuration_patch_instance.to_dict()
# create an instance of JsonApiCookieSecurityConfigurationPatch from a dict
json_api_cookie_security_configuration_patch_from_dict = JsonApiCookieSecurityConfigurationPatch.from_dict(json_api_cookie_security_configuration_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


