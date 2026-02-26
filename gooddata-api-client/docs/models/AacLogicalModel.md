# gooddata_api_client.model.aac_logical_model.AacLogicalModel

AAC logical data model representation compatible with Analytics-as-Code YAML format.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC logical data model representation compatible with Analytics-as-Code YAML format. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[datasets](#datasets)** | list, tuple,  | tuple,  | An array of datasets. | [optional] 
**[date_datasets](#date_datasets)** | list, tuple,  | tuple,  | An array of date datasets. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# datasets

An array of datasets.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of datasets. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacDataset**](AacDataset.md) | [**AacDataset**](AacDataset.md) | [**AacDataset**](AacDataset.md) |  | 

# date_datasets

An array of date datasets.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of date datasets. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacDateDataset**](AacDateDataset.md) | [**AacDateDataset**](AacDateDataset.md) | [**AacDateDataset**](AacDateDataset.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

