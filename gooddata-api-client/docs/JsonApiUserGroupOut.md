# JsonApiUserGroupOut

JSON:API representation of userGroup entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserGroupInAttributes**](JsonApiUserGroupInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiUserGroupInRelationships**](JsonApiUserGroupInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_user_group_out import JsonApiUserGroupOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserGroupOut from a JSON string
json_api_user_group_out_instance = JsonApiUserGroupOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserGroupOut.to_json())

# convert the object into a dict
json_api_user_group_out_dict = json_api_user_group_out_instance.to_dict()
# create an instance of JsonApiUserGroupOut from a dict
json_api_user_group_out_from_dict = JsonApiUserGroupOut.from_dict(json_api_user_group_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


