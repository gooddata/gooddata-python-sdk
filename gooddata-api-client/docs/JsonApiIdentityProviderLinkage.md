# JsonApiIdentityProviderLinkage

The \\\"type\\\" and \\\"id\\\" to non-empty members.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.json_api_identity_provider_linkage import JsonApiIdentityProviderLinkage

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiIdentityProviderLinkage from a JSON string
json_api_identity_provider_linkage_instance = JsonApiIdentityProviderLinkage.from_json(json)
# print the JSON string representation of the object
print(JsonApiIdentityProviderLinkage.to_json())

# convert the object into a dict
json_api_identity_provider_linkage_dict = json_api_identity_provider_linkage_instance.to_dict()
# create an instance of JsonApiIdentityProviderLinkage from a dict
json_api_identity_provider_linkage_from_dict = JsonApiIdentityProviderLinkage.from_dict(json_api_identity_provider_linkage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


