# JsonApiUserGroupInRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**parents** | [**JsonApiUserGroupInRelationshipsParents**](JsonApiUserGroupInRelationshipsParents.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_group_in_relationships import JsonApiUserGroupInRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserGroupInRelationships from a JSON string
json_api_user_group_in_relationships_instance = JsonApiUserGroupInRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserGroupInRelationships.to_json())

# convert the object into a dict
json_api_user_group_in_relationships_dict = json_api_user_group_in_relationships_instance.to_dict()
# create an instance of JsonApiUserGroupInRelationships from a dict
json_api_user_group_in_relationships_from_dict = JsonApiUserGroupInRelationships.from_dict(json_api_user_group_in_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


