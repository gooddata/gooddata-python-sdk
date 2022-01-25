# DeclarativeOrganizationInfo

Information available about an organization.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Identifier of the organization. | 
**name** | **str** | Formal name of the organization. | 
**hostname** | **str** | Formal hostname used in deployment. | 
**oauth_issuer_location** | **str** | URI of the authentication provider. | [optional] 
**oauth_client_id** | **str** | Identifier of the authentication provider | [optional] 
**oauth_client_secret** | **str** | Communication secret of the authentication provider (never returned back). | [optional] 
**permissions** | [**[DeclarativeOrganizationPermission]**](DeclarativeOrganizationPermission.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


