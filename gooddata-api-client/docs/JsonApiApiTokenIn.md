# JsonApiApiTokenIn

JSON:API representation of apiToken entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_api_token_in import JsonApiApiTokenIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiApiTokenIn from a JSON string
json_api_api_token_in_instance = JsonApiApiTokenIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiApiTokenIn.to_json())

# convert the object into a dict
json_api_api_token_in_dict = json_api_api_token_in_instance.to_dict()
# create an instance of JsonApiApiTokenIn from a dict
json_api_api_token_in_from_dict = JsonApiApiTokenIn.from_dict(json_api_api_token_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


