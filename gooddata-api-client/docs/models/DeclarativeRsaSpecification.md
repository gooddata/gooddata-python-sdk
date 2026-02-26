# gooddata_api_client.model.declarative_rsa_specification.DeclarativeRsaSpecification

Declarative specification of the cryptographic key.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Declarative specification of the cryptographic key. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**kty** | str,  | str,  | Key type parameter | must be one of ["RSA", ] 
**e** | str,  | str,  | parameter contains the exponent value for the RSA public key. | 
**use** | str,  | str,  | Parameter identifies the intended use of the public key. | must be one of ["sig", ] 
**kid** | str,  | str,  | Parameter is used to match a specific key. | 
**alg** | str,  | str,  | Algorithm intended for use with the key. | must be one of ["RS256", "RS384", "RS512", ] 
**n** | str,  | str,  | Parameter contains the modulus value for the RSA public key. | 
**[x5c](#x5c)** | list, tuple,  | tuple,  | Parameter contains a chain of one or more PKIX certificates. | [optional] 
**x5t** | str,  | str,  | Parameter is a base64url-encoded SHA-1 thumbprint of the DER encoding of an X.509 certificate. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# x5c

Parameter contains a chain of one or more PKIX certificates.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Parameter contains a chain of one or more PKIX certificates. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

