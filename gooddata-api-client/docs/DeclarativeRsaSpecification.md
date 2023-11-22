# DeclarativeRsaSpecification

Declarative specification of the cryptographic key.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alg** | **str** | Algorithm intended for use with the key. | 
**e** | **str** | parameter contains the exponent value for the RSA public key. | 
**kid** | **str** | Parameter is used to match a specific key. | 
**n** | **str** | Parameter contains the modulus value for the RSA public key. | 
**kty** | **str** | Key type parameter | defaults to "RSA"
**use** | **str** | Parameter identifies the intended use of the public key. | defaults to "sig"
**x5c** | **[str]** | Parameter contains a chain of one or more PKIX certificates. | [optional] 
**x5t** | **str** | Parameter is a base64url-encoded SHA-1 thumbprint of the DER encoding of an X.509 certificate. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


