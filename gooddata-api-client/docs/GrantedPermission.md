# GrantedPermission

Permissions granted to the user group

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**level** | **str** | Level of permission | 
**source** | **str** | Source of permission | 

## Example

```python
from gooddata_api_client.models.granted_permission import GrantedPermission

# TODO update the JSON string below
json = "{}"
# create an instance of GrantedPermission from a JSON string
granted_permission_instance = GrantedPermission.from_json(json)
# print the JSON string representation of the object
print(GrantedPermission.to_json())

# convert the object into a dict
granted_permission_dict = granted_permission_instance.to_dict()
# create an instance of GrantedPermission from a dict
granted_permission_from_dict = GrantedPermission.from_dict(granted_permission_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


