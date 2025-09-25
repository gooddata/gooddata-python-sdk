# JsonApiOrganizationInRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identity_provider** | [**JsonApiOrganizationInRelationshipsIdentityProvider**](JsonApiOrganizationInRelationshipsIdentityProvider.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_in_relationships import JsonApiOrganizationInRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationInRelationships from a JSON string
json_api_organization_in_relationships_instance = JsonApiOrganizationInRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationInRelationships.to_json())

# convert the object into a dict
json_api_organization_in_relationships_dict = json_api_organization_in_relationships_instance.to_dict()
# create an instance of JsonApiOrganizationInRelationships from a dict
json_api_organization_in_relationships_from_dict = JsonApiOrganizationInRelationships.from_dict(json_api_organization_in_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


