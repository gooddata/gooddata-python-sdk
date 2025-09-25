# JsonApiCookieSecurityConfigurationInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**last_rotation** | **datetime** |  | [optional] 
**rotation_interval** | **str** | Length of interval between automatic rotations expressed in format of ISO 8601 duration | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_cookie_security_configuration_in_attributes import JsonApiCookieSecurityConfigurationInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCookieSecurityConfigurationInAttributes from a JSON string
json_api_cookie_security_configuration_in_attributes_instance = JsonApiCookieSecurityConfigurationInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiCookieSecurityConfigurationInAttributes.to_json())

# convert the object into a dict
json_api_cookie_security_configuration_in_attributes_dict = json_api_cookie_security_configuration_in_attributes_instance.to_dict()
# create an instance of JsonApiCookieSecurityConfigurationInAttributes from a dict
json_api_cookie_security_configuration_in_attributes_from_dict = JsonApiCookieSecurityConfigurationInAttributes.from_dict(json_api_cookie_security_configuration_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


