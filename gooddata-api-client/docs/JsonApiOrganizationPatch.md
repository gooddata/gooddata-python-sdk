# JsonApiOrganizationPatch

JSON:API representation of patching organization entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationInAttributes**](JsonApiOrganizationInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiOrganizationInRelationships**](JsonApiOrganizationInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_organization_patch import JsonApiOrganizationPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationPatch from a JSON string
json_api_organization_patch_instance = JsonApiOrganizationPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationPatch.to_json())

# convert the object into a dict
json_api_organization_patch_dict = json_api_organization_patch_instance.to_dict()
# create an instance of JsonApiOrganizationPatch from a dict
json_api_organization_patch_from_dict = JsonApiOrganizationPatch.from_dict(json_api_organization_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


