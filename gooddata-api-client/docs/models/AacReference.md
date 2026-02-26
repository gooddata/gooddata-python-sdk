# gooddata_api_client.model.aac_reference.AacReference

AAC reference to another dataset.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC reference to another dataset. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[sources](#sources)** | list, tuple,  | tuple,  | Source columns for the reference. | 
**dataset** | str,  | str,  | Target dataset ID. | 
**multi_directional** | bool,  | BoolClass,  | Whether the reference is multi-directional. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# sources

Source columns for the reference.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Source columns for the reference. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacReferenceSource**](AacReferenceSource.md) | [**AacReferenceSource**](AacReferenceSource.md) | [**AacReferenceSource**](AacReferenceSource.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

