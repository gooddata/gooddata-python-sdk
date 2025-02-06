# JsonApiIdentityProviderPatchAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_claim_mapping** | **{str: (str,)}** | Map of custom claim overrides. To be used when your Idp does not provide default claims (sub, email, name, given_name, family_name, urn.gooddata.user_groups [optional]). Define the key pair for the claim you wish to override, where the key is the default name of the attribute and the value is your custom name for the given attribute. | [optional] 
**identifiers** | **[str]** | List of identifiers for this IdP, where an identifier is a domain name. Users with email addresses belonging to these domains will be authenticated by this IdP. In multiple provider setup, this field is mandatory. | [optional] 
**oauth_client_id** | **str** | The OAuth client id of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**oauth_client_secret** | **str** | The OAuth client secret of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**oauth_issuer_location** | **str** | The location of your OIDC provider. This field is mandatory for OIDC IdP. | [optional] 
**saml_metadata** | **str** | Base64 encoded xml document with SAML metadata. This document is issued by your SAML provider. It includes the issuer&#39;s name, expiration information, and keys that can be used to validate the response from the identity provider. This field is mandatory for SAML IdP. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


