# JsonApiIdentityProviderPatchAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifiers** | **[str]** | List of identifiers for this IdP, where an identifier is a domain name. Users with email addresses belonging to these domains will be authenticated by this IdP. In multiple provider setup, this field is mandatory. | [optional] 
**specification** | [**JsonApiIdentityProviderInAttributesSpecification**](JsonApiIdentityProviderInAttributesSpecification.md) |  | [optional] 
**type** | **str** | Type of the identity provider. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


