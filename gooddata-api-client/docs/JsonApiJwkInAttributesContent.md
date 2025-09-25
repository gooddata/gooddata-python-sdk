# JsonApiJwkInAttributesContent

Specification of the cryptographic key

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alg** | **str** |  | 
**e** | **str** |  | 
**kid** | **str** |  | 
**kty** | **str** |  | 
**n** | **str** |  | 
**use** | **str** |  | 
**x5c** | **List[str]** |  | [optional] 
**x5t** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_jwk_in_attributes_content import JsonApiJwkInAttributesContent

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiJwkInAttributesContent from a JSON string
json_api_jwk_in_attributes_content_instance = JsonApiJwkInAttributesContent.from_json(json)
# print the JSON string representation of the object
print(JsonApiJwkInAttributesContent.to_json())

# convert the object into a dict
json_api_jwk_in_attributes_content_dict = json_api_jwk_in_attributes_content_instance.to_dict()
# create an instance of JsonApiJwkInAttributesContent from a dict
json_api_jwk_in_attributes_content_from_dict = JsonApiJwkInAttributesContent.from_dict(json_api_jwk_in_attributes_content_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


