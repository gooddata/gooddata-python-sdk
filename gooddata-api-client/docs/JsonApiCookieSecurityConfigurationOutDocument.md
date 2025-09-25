# JsonApiCookieSecurityConfigurationOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiCookieSecurityConfigurationOut**](JsonApiCookieSecurityConfigurationOut.md) |  | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_cookie_security_configuration_out_document import JsonApiCookieSecurityConfigurationOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiCookieSecurityConfigurationOutDocument from a JSON string
json_api_cookie_security_configuration_out_document_instance = JsonApiCookieSecurityConfigurationOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiCookieSecurityConfigurationOutDocument.to_json())

# convert the object into a dict
json_api_cookie_security_configuration_out_document_dict = json_api_cookie_security_configuration_out_document_instance.to_dict()
# create an instance of JsonApiCookieSecurityConfigurationOutDocument from a dict
json_api_cookie_security_configuration_out_document_from_dict = JsonApiCookieSecurityConfigurationOutDocument.from_dict(json_api_cookie_security_configuration_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


