# DeclarativeOrganizationInfo

Information available about an organization.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**hostname** | **str** | Formal hostname used in deployment. | 
**id** | **str** | Identifier of the organization. | 
**name** | **str** | Formal name of the organization. | 
**permissions** | [**[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md) |  | 
**allowed_origins** | **[str]** |  | [optional] 
**color_palettes** | [**[DeclarativeColorPalette]**](DeclarativeColorPalette.md) | A list of color palettes. | [optional] 
**csp_directives** | [**[DeclarativeCspDirective]**](DeclarativeCspDirective.md) | A list of CSP directives. | [optional] 
**early_access** | **str** | Early access defined on level Organization | [optional] 
**early_access_values** | **[str]** | Early access defined on level Organization | [optional] 
**identity_provider** | [**DeclarativeIdentityProviderIdentifier**](DeclarativeIdentityProviderIdentifier.md) |  | [optional] 
**settings** | [**[DeclarativeSetting]**](DeclarativeSetting.md) | A list of organization settings. | [optional] 
**themes** | [**[DeclarativeTheme]**](DeclarativeTheme.md) | A list of themes. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


