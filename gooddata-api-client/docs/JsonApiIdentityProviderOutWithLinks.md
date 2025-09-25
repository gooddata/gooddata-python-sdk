# JsonApiIdentityProviderOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiIdentityProviderOutAttributes**](JsonApiIdentityProviderOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_identity_provider_out_with_links import JsonApiIdentityProviderOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiIdentityProviderOutWithLinks from a JSON string
json_api_identity_provider_out_with_links_instance = JsonApiIdentityProviderOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiIdentityProviderOutWithLinks.to_json())

# convert the object into a dict
json_api_identity_provider_out_with_links_dict = json_api_identity_provider_out_with_links_instance.to_dict()
# create an instance of JsonApiIdentityProviderOutWithLinks from a dict
json_api_identity_provider_out_with_links_from_dict = JsonApiIdentityProviderOutWithLinks.from_dict(json_api_identity_provider_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


