# gooddata_api_client.model.declarative_identity_provider.DeclarativeIdentityProvider

Notification channels.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Notification channels. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | FilterView object ID. | 
**[customClaimMapping](#customClaimMapping)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of custom claim overrides. To be used when your Idp does not provide default claims (sub, email, name, given_name, family_name, urn.gooddata.user_groups [optional]). Define the key pair for the claim you wish to override, where the key is the default name of the attribute and the value is your custom name for the given attribute. | [optional] 
**[identifiers](#identifiers)** | list, tuple,  | tuple,  | List of identifiers for this IdP, where an identifier is a domain name. Users with email addresses belonging to these domains will be authenticated by this IdP. | [optional] 
**idpType** | str,  | str,  | Type of IdP for management purposes. MANAGED_IDP represents a GoodData managed IdP used in single OIDC setup, which is protected from altering/deletion. FIM_IDP represents a GoodData managed IdP used in federated identity management setup, which is protected from altering/deletion. CUSTOM_IDP represents customer&#x27;s own IdP, protected from deletion if currently used by org for authentication, deletable otherwise. | [optional] must be one of ["MANAGED_IDP", "FIM_IDP", "DEX_IDP", "CUSTOM_IDP", ] 
**oauthClientId** | str,  | str,  | The OAuth client id of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**oauthClientSecret** | str,  | str,  | The OAuth client secret of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**[oauthCustomAuthAttributes](#oauthCustomAuthAttributes)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of additional authentication attributes that should be added to the OAuth2 authentication requests, where the key is the name of the attribute and the value is the value of the attribute. | [optional] 
**[oauthCustomScopes](#oauthCustomScopes)** | list, tuple, None,  | tuple, NoneClass,  | List of additional OAuth scopes which may be required by other providers (e.g. Snowflake) | [optional] 
**oauthIssuerId** | str,  | str,  | Any string identifying the OIDC provider. This value is used as suffix for OAuth2 callback (redirect) URL. If not defined, the standard callback URL is used. This value is valid only for external OIDC providers, not for the internal DEX provider. | [optional] 
**oauthIssuerLocation** | str,  | str,  | The location of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**oauthSubjectIdClaim** | str,  | str,  | Any string identifying the claim in ID token, that should be used for user identification. The default value is &#x27;sub&#x27;. | [optional] 
**samlMetadata** | str,  | str,  | Base64 encoded xml document with SAML metadata. This document is issued by your SAML provider. It includes the issuer&#x27;s name, expiration information, and keys that can be used to validate the response from the identity provider. This field is mandatory for SAML IdP. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# customClaimMapping

Map of custom claim overrides. To be used when your Idp does not provide default claims (sub, email, name, given_name, family_name, urn.gooddata.user_groups [optional]). Define the key pair for the claim you wish to override, where the key is the default name of the attribute and the value is your custom name for the given attribute.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of custom claim overrides. To be used when your Idp does not provide default claims (sub, email, name, given_name, family_name, urn.gooddata.user_groups [optional]). Define the key pair for the claim you wish to override, where the key is the default name of the attribute and the value is your custom name for the given attribute. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type | [optional] 

# identifiers

List of identifiers for this IdP, where an identifier is a domain name. Users with email addresses belonging to these domains will be authenticated by this IdP.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of identifiers for this IdP, where an identifier is a domain name. Users with email addresses belonging to these domains will be authenticated by this IdP. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | List of identifiers for this IdP, where an identifier is a domain name. Users with email addresses belonging to these domains will be authenticated by this IdP. | 

# oauthCustomAuthAttributes

Map of additional authentication attributes that should be added to the OAuth2 authentication requests, where the key is the name of the attribute and the value is the value of the attribute.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of additional authentication attributes that should be added to the OAuth2 authentication requests, where the key is the name of the attribute and the value is the value of the attribute. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | str,  | str,  | any string name can be used but the value must be the correct type Map of additional authentication attributes that should be added to the OAuth2 authentication requests, where the key is the name of the attribute and the value is the value of the attribute. | [optional] 

# oauthCustomScopes

List of additional OAuth scopes which may be required by other providers (e.g. Snowflake)

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple, None,  | tuple, NoneClass,  | List of additional OAuth scopes which may be required by other providers (e.g. Snowflake) | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

