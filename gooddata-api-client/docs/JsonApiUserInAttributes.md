# JsonApiUserInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**authentication_id** | **str** |  | [optional] 
**email** | **str** |  | [optional] 
**firstname** | **str** |  | [optional] 
**lastname** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_in_attributes import JsonApiUserInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserInAttributes from a JSON string
json_api_user_in_attributes_instance = JsonApiUserInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserInAttributes.to_json())

# convert the object into a dict
json_api_user_in_attributes_dict = json_api_user_in_attributes_instance.to_dict()
# create an instance of JsonApiUserInAttributes from a dict
json_api_user_in_attributes_from_dict = JsonApiUserInAttributes.from_dict(json_api_user_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


