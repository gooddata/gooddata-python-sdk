# DeclarativeIdentityProviderIdentifier

An Identity Provider identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of the identity provider. | 
**type** | **str** | A type. | 

## Example

```python
from gooddata_api_client.models.declarative_identity_provider_identifier import DeclarativeIdentityProviderIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeIdentityProviderIdentifier from a JSON string
declarative_identity_provider_identifier_instance = DeclarativeIdentityProviderIdentifier.from_json(json)
# print the JSON string representation of the object
print(DeclarativeIdentityProviderIdentifier.to_json())

# convert the object into a dict
declarative_identity_provider_identifier_dict = declarative_identity_provider_identifier_instance.to_dict()
# create an instance of DeclarativeIdentityProviderIdentifier from a dict
declarative_identity_provider_identifier_from_dict = DeclarativeIdentityProviderIdentifier.from_dict(declarative_identity_provider_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


