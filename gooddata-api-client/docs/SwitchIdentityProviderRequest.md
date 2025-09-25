# SwitchIdentityProviderRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**idp_id** | **str** | Identity provider ID to set as active for the organization. | 

## Example

```python
from gooddata_api_client.models.switch_identity_provider_request import SwitchIdentityProviderRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SwitchIdentityProviderRequest from a JSON string
switch_identity_provider_request_instance = SwitchIdentityProviderRequest.from_json(json)
# print the JSON string representation of the object
print(SwitchIdentityProviderRequest.to_json())

# convert the object into a dict
switch_identity_provider_request_dict = switch_identity_provider_request_instance.to_dict()
# create an instance of SwitchIdentityProviderRequest from a dict
switch_identity_provider_request_from_dict = SwitchIdentityProviderRequest.from_dict(switch_identity_provider_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


