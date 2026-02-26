# gooddata_api_client.model.aac_date_dataset.AacDateDataset

AAC date dataset definition.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC date dataset definition. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Unique identifier of the date dataset. | 
**type** | str,  | str,  | Dataset type discriminator. | 
**description** | str,  | str,  | Date dataset description. | [optional] 
**[granularities](#granularities)** | list, tuple,  | tuple,  | List of granularities. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | Metadata tags. | [optional] 
**title** | str,  | str,  | Human readable title. | [optional] 
**title_base** | str,  | str,  | Title base for formatting. | [optional] 
**title_pattern** | str,  | str,  | Title pattern for formatting. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# granularities

List of granularities.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of granularities. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | List of granularities. | 

# tags

Metadata tags.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Metadata tags. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Metadata tags. | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

