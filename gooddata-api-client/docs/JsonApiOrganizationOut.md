# JsonApiOrganizationOut

JSON:API representation of organization entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationOutAttributes**](JsonApiOrganizationOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiOrganizationOutMeta**](JsonApiOrganizationOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiOrganizationOutRelationships**](JsonApiOrganizationOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_organization_out import JsonApiOrganizationOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationOut from a JSON string
json_api_organization_out_instance = JsonApiOrganizationOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationOut.to_json())

# convert the object into a dict
json_api_organization_out_dict = json_api_organization_out_instance.to_dict()
# create an instance of JsonApiOrganizationOut from a dict
json_api_organization_out_from_dict = JsonApiOrganizationOut.from_dict(json_api_organization_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


