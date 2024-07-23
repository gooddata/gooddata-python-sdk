# JsonApiOrganizationOutAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_origins** | **[str]** |  | [optional] 
**cache_settings** | [**JsonApiOrganizationOutAttributesCacheSettings**](JsonApiOrganizationOutAttributesCacheSettings.md) |  | [optional] 
**early_access** | **str, none_type** | The early access feature identifier. It is used to enable experimental features. Deprecated in favor of earlyAccessValues. | [optional] 
**early_access_values** | **[str], none_type** | The early access feature identifiers. They are used to enable experimental features. | [optional] 
**hostname** | **str** |  | [optional] 
**jit_enabled** | **bool** | Flag to enable/disable JIT provisioning in the given organization | [optional] 
**name** | **str, none_type** |  | [optional] 
**oauth_client_id** | **str** |  | [optional] 
**oauth_issuer_id** | **str** | Any string identifying the OIDC provider. This value is used as suffix for OAuth2 callback (redirect) URL. If not defined, the standard callback URL is used. This value is valid only for external OIDC providers, not for the internal DEX provider. | [optional] 
**oauth_issuer_location** | **str** |  | [optional] 
**oauth_subject_id_claim** | **str** | Any string identifying the claim in ID token, that should be used for user identification. The default value is &#39;sub&#39;. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


