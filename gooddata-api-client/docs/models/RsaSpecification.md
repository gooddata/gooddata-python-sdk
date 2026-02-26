# gooddata_api_client.model.rsa_specification.RsaSpecification

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**kty** | str,  | str,  |  | must be one of ["RSA", ] 
**e** | str,  | str,  |  | 
**use** | str,  | str,  |  | must be one of ["sig", ] 
**kid** | str,  | str,  |  | 
**alg** | str,  | str,  |  | must be one of ["RS256", "RS384", "RS512", ] 
**n** | str,  | str,  |  | 
**[x5c](#x5c)** | list, tuple,  | tuple,  |  | [optional] 
**x5t** | str,  | str,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# x5c

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

