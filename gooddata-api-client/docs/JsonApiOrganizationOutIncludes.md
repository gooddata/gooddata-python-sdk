# JsonApiOrganizationOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiIdentityProviderOutAttributes**](JsonApiIdentityProviderOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiUserGroupInRelationships**](JsonApiUserGroupInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_organization_out_includes import JsonApiOrganizationOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationOutIncludes from a JSON string
json_api_organization_out_includes_instance = JsonApiOrganizationOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationOutIncludes.to_json())

# convert the object into a dict
json_api_organization_out_includes_dict = json_api_organization_out_includes_instance.to_dict()
# create an instance of JsonApiOrganizationOutIncludes from a dict
json_api_organization_out_includes_from_dict = JsonApiOrganizationOutIncludes.from_dict(json_api_organization_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


