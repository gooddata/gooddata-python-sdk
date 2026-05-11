# DeclarativeIpAllowlistPolicy

A declarative form of an IP allowlist policy.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**allowed_sources** | **[str]** | Allowed source IP addresses or CIDR ranges. | 
**id** | **str** | Identifier of an IP allowlist policy. | 
**user_groups** | [**[DeclarativeUserGroupIdentifier]**](DeclarativeUserGroupIdentifier.md) | Target user groups this policy applies to. | [optional] 
**users** | [**[DeclarativeUserIdentifier]**](DeclarativeUserIdentifier.md) | Target users this policy applies to. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


