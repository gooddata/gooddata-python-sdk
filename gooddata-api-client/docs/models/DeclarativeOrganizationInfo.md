# gooddata_api_client.model.declarative_organization_info.DeclarativeOrganizationInfo

Information available about an organization.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Information available about an organization. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**hostname** | str,  | str,  | Formal hostname used in deployment. | 
**[permissions](#permissions)** | list, tuple,  | tuple,  |  | 
**name** | str,  | str,  | Formal name of the organization. | 
**id** | str,  | str,  | Identifier of the organization. | 
**[colorPalettes](#colorPalettes)** | list, tuple,  | tuple,  | A list of color palettes. | [optional] 
**[cspDirectives](#cspDirectives)** | list, tuple,  | tuple,  | A list of CSP directives. | [optional] 
**earlyAccess** | str,  | str,  | Early access defined on level Organization | [optional] 
**oauthClientId** | str,  | str,  | Identifier of the authentication provider | [optional] 
**oauthClientSecret** | str,  | str,  | Communication secret of the authentication provider (never returned back). | [optional] 
**oauthIssuerId** | str,  | str,  | Any string identifying the OIDC provider. This value is used as suffix for OAuth2 callback (redirect) URL. If not defined, the standard callback URL is used. This value is valid only for external OIDC providers, not for the internal DEX provider. | [optional] 
**oauthIssuerLocation** | str,  | str,  | URI of the authentication provider. | [optional] 
**[settings](#settings)** | list, tuple,  | tuple,  | A list of organization settings. | [optional] 
**[themes](#themes)** | list, tuple,  | tuple,  | A list of themes. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# permissions

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeOrganizationPermission**](DeclarativeOrganizationPermission.md) | [**DeclarativeOrganizationPermission**](DeclarativeOrganizationPermission.md) | [**DeclarativeOrganizationPermission**](DeclarativeOrganizationPermission.md) |  | 

# colorPalettes

A list of color palettes.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of color palettes. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeColorPalette**](DeclarativeColorPalette.md) | [**DeclarativeColorPalette**](DeclarativeColorPalette.md) | [**DeclarativeColorPalette**](DeclarativeColorPalette.md) |  | 

# cspDirectives

A list of CSP directives.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of CSP directives. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeCspDirective**](DeclarativeCspDirective.md) | [**DeclarativeCspDirective**](DeclarativeCspDirective.md) | [**DeclarativeCspDirective**](DeclarativeCspDirective.md) |  | 

# settings

A list of organization settings.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of organization settings. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeSetting**](DeclarativeSetting.md) | [**DeclarativeSetting**](DeclarativeSetting.md) | [**DeclarativeSetting**](DeclarativeSetting.md) |  | 

# themes

A list of themes.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of themes. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeTheme**](DeclarativeTheme.md) | [**DeclarativeTheme**](DeclarativeTheme.md) | [**DeclarativeTheme**](DeclarativeTheme.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

