# JsonApiJwkInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**JsonApiJwkInAttributesContent**](JsonApiJwkInAttributesContent.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_jwk_in_attributes import JsonApiJwkInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiJwkInAttributes from a JSON string
json_api_jwk_in_attributes_instance = JsonApiJwkInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiJwkInAttributes.to_json())

# convert the object into a dict
json_api_jwk_in_attributes_dict = json_api_jwk_in_attributes_instance.to_dict()
# create an instance of JsonApiJwkInAttributes from a dict
json_api_jwk_in_attributes_from_dict = JsonApiJwkInAttributes.from_dict(json_api_jwk_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


