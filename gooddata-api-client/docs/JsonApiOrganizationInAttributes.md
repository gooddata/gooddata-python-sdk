# JsonApiOrganizationInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_origins** | **List[str]** |  | [optional] 
**early_access** | **str** | The early access feature identifier. It is used to enable experimental features. Deprecated in favor of earlyAccessValues. | [optional] 
**early_access_values** | **List[str]** | The early access feature identifiers. They are used to enable experimental features. | [optional] 
**hostname** | **str** |  | [optional] 
**name** | **str** |  | [optional] 
**oauth_client_id** | **str** |  | [optional] 
**oauth_client_secret** | **str** |  | [optional] 
**oauth_custom_auth_attributes** | **Dict[str, str]** | Map of additional authentication attributes that should be added to the OAuth2 authentication requests, where the key is the name of the attribute and the value is the value of the attribute. | [optional] 
**oauth_custom_scopes** | **List[str]** | List of additional OAuth scopes which may be required by other providers (e.g. Snowflake) | [optional] 
**oauth_issuer_id** | **str** | Any string identifying the OIDC provider. This value is used as suffix for OAuth2 callback (redirect) URL. If not defined, the standard callback URL is used. This value is valid only for external OIDC providers, not for the internal DEX provider. | [optional] 
**oauth_issuer_location** | **str** |  | [optional] 
**oauth_subject_id_claim** | **str** | Any string identifying the claim in ID token, that should be used for user identification. The default value is &#39;sub&#39;. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_in_attributes import JsonApiOrganizationInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationInAttributes from a JSON string
json_api_organization_in_attributes_instance = JsonApiOrganizationInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationInAttributes.to_json())

# convert the object into a dict
json_api_organization_in_attributes_dict = json_api_organization_in_attributes_instance.to_dict()
# create an instance of JsonApiOrganizationInAttributes from a dict
json_api_organization_in_attributes_from_dict = JsonApiOrganizationInAttributes.from_dict(json_api_organization_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


