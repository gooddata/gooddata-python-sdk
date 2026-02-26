# gooddata_api_client.model.aac_label.AacLabel

AAC label definition.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC label definition. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**data_type** | str,  | str,  | Data type of the column. | [optional] must be one of ["INT", "STRING", "DATE", "NUMERIC", "TIMESTAMP", "TIMESTAMP_TZ", "BOOLEAN", ] 
**description** | str,  | str,  | Label description. | [optional] 
**geo_area_config** | [**AacGeoAreaConfig**](AacGeoAreaConfig.md) | [**AacGeoAreaConfig**](AacGeoAreaConfig.md) |  | [optional] 
**is_hidden** | bool,  | BoolClass,  | Deprecated. Use showInAiResults instead. | [optional] 
**locale** | str,  | str,  | Locale for sorting. | [optional] 
**show_in_ai_results** | bool,  | BoolClass,  | Whether to show in AI results. | [optional] 
**source_column** | str,  | str,  | Source column name. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | Metadata tags. | [optional] 
**title** | str,  | str,  | Human readable title. | [optional] 
**[translations](#translations)** | list, tuple,  | tuple,  | Localized source columns. | [optional] 
**value_type** | str,  | str,  | Value type. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

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

# translations

Localized source columns.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Localized source columns. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacLabelTranslation**](AacLabelTranslation.md) | [**AacLabelTranslation**](AacLabelTranslation.md) | [**AacLabelTranslation**](AacLabelTranslation.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

