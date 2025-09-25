# JsonApiApiTokenOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**bearer_token** | **str** | The value of the Bearer token. It is only returned when the API token is created. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_api_token_out_attributes import JsonApiApiTokenOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiApiTokenOutAttributes from a JSON string
json_api_api_token_out_attributes_instance = JsonApiApiTokenOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiApiTokenOutAttributes.to_json())

# convert the object into a dict
json_api_api_token_out_attributes_dict = json_api_api_token_out_attributes_instance.to_dict()
# create an instance of JsonApiApiTokenOutAttributes from a dict
json_api_api_token_out_attributes_from_dict = JsonApiApiTokenOutAttributes.from_dict(json_api_api_token_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


