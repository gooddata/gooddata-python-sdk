# JsonApiIdentityProviderOutAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_claim_mapping** | **{str: (str,)}** | Map of custom claim overrides. To be used when your Idp does not provide default claims (sub, email, name, given_name, family_name). Define the key pair for the claim you wish to override, where the key is the default name of the attribute and the value is your custom name for the given attribute. | [optional] 
**identifiers** | **[str]** | List of identifiers for this IdP, where an identifier is a domain name. Users with email addresses belonging to these domains will be authenticated by this IdP. | [optional] 
**idp_type** | **str** | Type of IdP for management purposes. MANAGED_IDP represents a GoodData managed IdP used in single OIDC setup, which is protected from altering/deletion. FIM_IDP represents a GoodData managed IdP used in federated identity management setup, which is protected from altering/deletion. CUSTOM_IDP represents customer&#39;s own IdP, protected from deletion if currently used by org for authentication, deletable otherwise. | [optional] 
**oauth_client_id** | **str** | The OAuth client id of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**oauth_custom_auth_attributes** | **{str: (str,)}** | Map of additional authentication attributes that should be added to the OAuth2 authentication requests, where the key is the name of the attribute and the value is the value of the attribute. | [optional] 
**oauth_custom_scopes** | **[str], none_type** | List of additional OAuth scopes which may be required by other providers (e.g. Snowflake) | [optional] 
**oauth_issuer_id** | **str** | Any string identifying the OIDC provider. This value is used as suffix for OAuth2 callback (redirect) URL. If not defined, the standard callback URL is used. This value is valid only for external OIDC providers, not for the internal DEX provider. | [optional] 
**oauth_issuer_location** | **str** | The location of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**oauth_subject_id_claim** | **str** | Any string identifying the claim in ID token, that should be used for user identification. The default value is &#39;sub&#39;. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


