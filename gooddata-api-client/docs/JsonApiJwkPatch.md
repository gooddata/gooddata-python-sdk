# JsonApiJwkPatch

JSON:API representation of patching jwk entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiJwkInAttributes**](JsonApiJwkInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_jwk_patch import JsonApiJwkPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiJwkPatch from a JSON string
json_api_jwk_patch_instance = JsonApiJwkPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiJwkPatch.to_json())

# convert the object into a dict
json_api_jwk_patch_dict = json_api_jwk_patch_instance.to_dict()
# create an instance of JsonApiJwkPatch from a dict
json_api_jwk_patch_from_dict = JsonApiJwkPatch.from_dict(json_api_jwk_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


