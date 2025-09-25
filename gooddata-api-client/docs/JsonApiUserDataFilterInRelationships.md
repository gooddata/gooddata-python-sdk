# JsonApiUserDataFilterInRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user** | [**JsonApiFilterViewInRelationshipsUser**](JsonApiFilterViewInRelationshipsUser.md) |  | [optional] 
**user_group** | [**JsonApiOrganizationOutRelationshipsBootstrapUserGroup**](JsonApiOrganizationOutRelationshipsBootstrapUserGroup.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_in_relationships import JsonApiUserDataFilterInRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterInRelationships from a JSON string
json_api_user_data_filter_in_relationships_instance = JsonApiUserDataFilterInRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterInRelationships.to_json())

# convert the object into a dict
json_api_user_data_filter_in_relationships_dict = json_api_user_data_filter_in_relationships_instance.to_dict()
# create an instance of JsonApiUserDataFilterInRelationships from a dict
json_api_user_data_filter_in_relationships_from_dict = JsonApiUserDataFilterInRelationships.from_dict(json_api_user_data_filter_in_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


