# DeclarativeOrganizationInfo

Information available about an organization.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_origins** | **List[str]** |  | [optional] 
**color_palettes** | [**List[DeclarativeColorPalette]**](DeclarativeColorPalette.md) | A list of color palettes. | [optional] 
**csp_directives** | [**List[DeclarativeCspDirective]**](DeclarativeCspDirective.md) | A list of CSP directives. | [optional] 
**early_access** | **str** | Early access defined on level Organization | [optional] 
**early_access_values** | **List[str]** | Early access defined on level Organization | [optional] 
**hostname** | **str** | Formal hostname used in deployment. | 
**id** | **str** | Identifier of the organization. | 
**identity_provider** | [**DeclarativeIdentityProviderIdentifier**](DeclarativeIdentityProviderIdentifier.md) |  | [optional] 
**name** | **str** | Formal name of the organization. | 
**oauth_client_id** | **str** | Identifier of the authentication provider | [optional] 
**oauth_client_secret** | **str** | Communication secret of the authentication provider (never returned back). | [optional] 
**oauth_custom_auth_attributes** | **Dict[str, str]** | Map of additional authentication attributes that should be added to the OAuth2 authentication requests, where the key is the name of the attribute and the value is the value of the attribute. | [optional] 
**oauth_custom_scopes** | **List[str]** | List of additional OAuth scopes which may be required by other providers (e.g. Snowflake) | [optional] 
**oauth_issuer_id** | **str** | Any string identifying the OIDC provider. This value is used as suffix for OAuth2 callback (redirect) URL. If not defined, the standard callback URL is used. This value is valid only for external OIDC providers, not for the internal DEX provider. | [optional] 
**oauth_issuer_location** | **str** | URI of the authentication provider. | [optional] 
**oauth_subject_id_claim** | **str** | Any string identifying the claim in ID token, that should be used for user identification. The default value is &#39;sub&#39;. | [optional] 
**permissions** | [**List[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md) |  | 
**settings** | [**List[DeclarativeSetting]**](DeclarativeSetting.md) | A list of organization settings. | [optional] 
**themes** | [**List[DeclarativeTheme]**](DeclarativeTheme.md) | A list of themes. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_organization_info import DeclarativeOrganizationInfo

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeOrganizationInfo from a JSON string
declarative_organization_info_instance = DeclarativeOrganizationInfo.from_json(json)
# print the JSON string representation of the object
print(DeclarativeOrganizationInfo.to_json())

# convert the object into a dict
declarative_organization_info_dict = declarative_organization_info_instance.to_dict()
# create an instance of DeclarativeOrganizationInfo from a dict
declarative_organization_info_from_dict = DeclarativeOrganizationInfo.from_dict(declarative_organization_info_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


