# DeclarativeOrganizationInfo

Information available about an organization.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hostname** | **str** | Formal hostname used in deployment. | 
**id** | **str** | Identifier of the organization. | 
**name** | **str** | Formal name of the organization. | 
**permissions** | [**[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md) |  | 
**color_palettes** | [**[DeclarativeColorPalette]**](DeclarativeColorPalette.md) | A list of color palettes. | [optional] 
**csp_directives** | [**[DeclarativeCspDirective]**](DeclarativeCspDirective.md) | A list of CSP directives. | [optional] 
**early_access** | **str** | Early access defined on level Organization | [optional] 
**oauth_client_id** | **str** | Identifier of the authentication provider | [optional] 
**oauth_client_secret** | **str** | Communication secret of the authentication provider (never returned back). | [optional] 
**oauth_issuer_id** | **str** | Any string identifying the OIDC provider. This value is used as suffix for OAuth2 callback (redirect) URL. If not defined, the standard callback URL is used. This value is valid only for external OIDC providers, not for the internal DEX provider. | [optional] 
**oauth_issuer_location** | **str** | URI of the authentication provider. | [optional] 
**settings** | [**[DeclarativeSetting]**](DeclarativeSetting.md) | A list of organization settings. | [optional] 
**themes** | [**[DeclarativeTheme]**](DeclarativeTheme.md) | A list of themes. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


