# DeclarativeRsaSpecification

Declarative specification of the cryptographic key.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alg** | **str** | Algorithm intended for use with the key. | 
**e** | **str** | parameter contains the exponent value for the RSA public key. | 
**kid** | **str** | Parameter is used to match a specific key. | 
**kty** | **str** | Key type parameter | 
**n** | **str** | Parameter contains the modulus value for the RSA public key. | 
**use** | **str** | Parameter identifies the intended use of the public key. | 
**x5c** | **List[str]** | Parameter contains a chain of one or more PKIX certificates. | [optional] 
**x5t** | **str** | Parameter is a base64url-encoded SHA-1 thumbprint of the DER encoding of an X.509 certificate. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_rsa_specification import DeclarativeRsaSpecification

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeRsaSpecification from a JSON string
declarative_rsa_specification_instance = DeclarativeRsaSpecification.from_json(json)
# print the JSON string representation of the object
print(DeclarativeRsaSpecification.to_json())

# convert the object into a dict
declarative_rsa_specification_dict = declarative_rsa_specification_instance.to_dict()
# create an instance of DeclarativeRsaSpecification from a dict
declarative_rsa_specification_from_dict = DeclarativeRsaSpecification.from_dict(declarative_rsa_specification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


