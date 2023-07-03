# JsonApiJwkInAttributesContent

Specification of the cryptographic key

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alg** | **str** |  | [optional] 
**e** | **str** |  | [optional] 
**kid** | **str** |  | [optional] 
**kty** | **str** |  | [optional]  if omitted the server will use the default value of "RSA"
**n** | **str** |  | [optional] 
**use** | **str** |  | [optional]  if omitted the server will use the default value of "sig"
**x5c** | **[str]** |  | [optional] 
**x5t** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


