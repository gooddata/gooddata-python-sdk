# JsonApiOrganizationOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bootstrap_user** | [**JsonApiFilterViewInRelationshipsUser**](JsonApiFilterViewInRelationshipsUser.md) |  | [optional] 
**bootstrap_user_group** | [**JsonApiOrganizationOutRelationshipsBootstrapUserGroup**](JsonApiOrganizationOutRelationshipsBootstrapUserGroup.md) |  | [optional] 
**identity_provider** | [**JsonApiOrganizationInRelationshipsIdentityProvider**](JsonApiOrganizationInRelationshipsIdentityProvider.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_out_relationships import JsonApiOrganizationOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationOutRelationships from a JSON string
json_api_organization_out_relationships_instance = JsonApiOrganizationOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationOutRelationships.to_json())

# convert the object into a dict
json_api_organization_out_relationships_dict = json_api_organization_out_relationships_instance.to_dict()
# create an instance of JsonApiOrganizationOutRelationships from a dict
json_api_organization_out_relationships_from_dict = JsonApiOrganizationOutRelationships.from_dict(json_api_organization_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


