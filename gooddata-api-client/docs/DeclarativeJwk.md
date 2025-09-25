# DeclarativeJwk

A declarative form of the JWK.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | [**DeclarativeJwkSpecification**](DeclarativeJwkSpecification.md) |  | 
**id** | **str** | JWK object ID. | 

## Example

```python
from gooddata_api_client.models.declarative_jwk import DeclarativeJwk

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeJwk from a JSON string
declarative_jwk_instance = DeclarativeJwk.from_json(json)
# print the JSON string representation of the object
print(DeclarativeJwk.to_json())

# convert the object into a dict
declarative_jwk_dict = declarative_jwk_instance.to_dict()
# create an instance of DeclarativeJwk from a dict
declarative_jwk_from_dict = DeclarativeJwk.from_dict(declarative_jwk_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


