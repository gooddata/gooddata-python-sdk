# DeclarativeOrganizationPermission

Definition of an organization permission assigned to a user/user-group.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**assignee** | [**AssigneeIdentifier**](AssigneeIdentifier.md) |  | 
**name** | **str** | Permission name. | 

## Example

```python
from gooddata_api_client.models.declarative_organization_permission import DeclarativeOrganizationPermission

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeOrganizationPermission from a JSON string
declarative_organization_permission_instance = DeclarativeOrganizationPermission.from_json(json)
# print the JSON string representation of the object
print(DeclarativeOrganizationPermission.to_json())

# convert the object into a dict
declarative_organization_permission_dict = declarative_organization_permission_instance.to_dict()
# create an instance of DeclarativeOrganizationPermission from a dict
declarative_organization_permission_from_dict = DeclarativeOrganizationPermission.from_dict(declarative_organization_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


