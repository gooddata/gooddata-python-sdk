# JsonApiIdentityProviderIn

JSON:API representation of identityProvider entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiIdentityProviderInAttributes**](JsonApiIdentityProviderInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_identity_provider_in import JsonApiIdentityProviderIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiIdentityProviderIn from a JSON string
json_api_identity_provider_in_instance = JsonApiIdentityProviderIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiIdentityProviderIn.to_json())

# convert the object into a dict
json_api_identity_provider_in_dict = json_api_identity_provider_in_instance.to_dict()
# create an instance of JsonApiIdentityProviderIn from a dict
json_api_identity_provider_in_from_dict = JsonApiIdentityProviderIn.from_dict(json_api_identity_provider_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


