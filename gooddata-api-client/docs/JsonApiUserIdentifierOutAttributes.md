# JsonApiUserIdentifierOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**email** | **str** |  | [optional] 
**firstname** | **str** |  | [optional] 
**lastname** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_identifier_out_attributes import JsonApiUserIdentifierOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserIdentifierOutAttributes from a JSON string
json_api_user_identifier_out_attributes_instance = JsonApiUserIdentifierOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserIdentifierOutAttributes.to_json())

# convert the object into a dict
json_api_user_identifier_out_attributes_dict = json_api_user_identifier_out_attributes_instance.to_dict()
# create an instance of JsonApiUserIdentifierOutAttributes from a dict
json_api_user_identifier_out_attributes_from_dict = JsonApiUserIdentifierOutAttributes.from_dict(json_api_user_identifier_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


