# RsaSpecification


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
from gooddata_api_client.models.rsa_specification import RsaSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of RsaSpecification from a JSON string
rsa_specification_instance = RsaSpecification.from_json(json)
# print the JSON string representation of the object
print(RsaSpecification.to_json())

# convert the object into a dict
rsa_specification_dict = rsa_specification_instance.to_dict()
# create an instance of RsaSpecification from a dict
rsa_specification_from_dict = RsaSpecification.from_dict(rsa_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


