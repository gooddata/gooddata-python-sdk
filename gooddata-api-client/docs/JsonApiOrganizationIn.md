# JsonApiOrganizationIn

JSON:API representation of organization entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiOrganizationInAttributes**](JsonApiOrganizationInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiOrganizationInRelationships**](JsonApiOrganizationInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_organization_in import JsonApiOrganizationIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiOrganizationIn from a JSON string
json_api_organization_in_instance = JsonApiOrganizationIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiOrganizationIn.to_json())

# convert the object into a dict
json_api_organization_in_dict = json_api_organization_in_instance.to_dict()
# create an instance of JsonApiOrganizationIn from a dict
json_api_organization_in_from_dict = JsonApiOrganizationIn.from_dict(json_api_organization_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


