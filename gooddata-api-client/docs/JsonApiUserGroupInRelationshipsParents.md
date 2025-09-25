# JsonApiUserGroupInRelationshipsParents


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiUserGroupLinkage]**](JsonApiUserGroupLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_user_group_in_relationships_parents import JsonApiUserGroupInRelationshipsParents

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserGroupInRelationshipsParents from a JSON string
json_api_user_group_in_relationships_parents_instance = JsonApiUserGroupInRelationshipsParents.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserGroupInRelationshipsParents.to_json())

# convert the object into a dict
json_api_user_group_in_relationships_parents_dict = json_api_user_group_in_relationships_parents_instance.to_dict()
# create an instance of JsonApiUserGroupInRelationshipsParents from a dict
json_api_user_group_in_relationships_parents_from_dict = JsonApiUserGroupInRelationshipsParents.from_dict(json_api_user_group_in_relationships_parents_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


