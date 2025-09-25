# DeclarativeOrganization

Complete definition of an organization in a declarative form.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sources** | [**List[DeclarativeDataSource]**](DeclarativeDataSource.md) |  | [optional] 
**export_templates** | [**List[DeclarativeExportTemplate]**](DeclarativeExportTemplate.md) |  | [optional] 
**identity_providers** | [**List[DeclarativeIdentityProvider]**](DeclarativeIdentityProvider.md) |  | [optional] 
**jwks** | [**List[DeclarativeJwk]**](DeclarativeJwk.md) |  | [optional] 
**notification_channels** | [**List[DeclarativeNotificationChannel]**](DeclarativeNotificationChannel.md) |  | [optional] 
**organization** | [**DeclarativeOrganizationInfo**](DeclarativeOrganizationInfo.md) |  | 
**user_groups** | [**List[DeclarativeUserGroup]**](DeclarativeUserGroup.md) |  | [optional] 
**users** | [**List[DeclarativeUser]**](DeclarativeUser.md) |  | [optional] 
**workspace_data_filters** | [**List[DeclarativeWorkspaceDataFilter]**](DeclarativeWorkspaceDataFilter.md) |  | [optional] 
**workspaces** | [**List[DeclarativeWorkspace]**](DeclarativeWorkspace.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_organization import DeclarativeOrganization

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeOrganization from a JSON string
declarative_organization_instance = DeclarativeOrganization.from_json(json)
# print the JSON string representation of the object
print(DeclarativeOrganization.to_json())

# convert the object into a dict
declarative_organization_dict = declarative_organization_instance.to_dict()
# create an instance of DeclarativeOrganization from a dict
declarative_organization_from_dict = DeclarativeOrganization.from_dict(declarative_organization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


