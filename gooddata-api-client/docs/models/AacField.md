# gooddata_api_client.model.aac_field.AacField

AAC field definition (attribute, fact, or aggregated_fact).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC field definition (attribute, fact, or aggregated_fact). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**type** | str,  | str,  | Field type. | 
**aggregated_as** | str,  | str,  | Aggregation method. | [optional] 
**assigned_to** | str,  | str,  | Source fact ID for aggregated fact. | [optional] 
**data_type** | str,  | str,  | Data type of the column. | [optional] must be one of ["INT", "STRING", "DATE", "NUMERIC", "TIMESTAMP", "TIMESTAMP_TZ", "BOOLEAN", ] 
**default_view** | str,  | str,  | Default view label ID. | [optional] 
**description** | str,  | str,  | Field description. | [optional] 
**is_hidden** | bool,  | BoolClass,  | Deprecated. Use showInAiResults instead. | [optional] 
**[labels](#labels)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Attribute labels. | [optional] 
**locale** | str,  | str,  | Locale for sorting. | [optional] 
**show_in_ai_results** | bool,  | BoolClass,  | Whether to show in AI results. | [optional] 
**sort_column** | str,  | str,  | Sort column name. | [optional] 
**sort_direction** | str,  | str,  | Sort direction. | [optional] must be one of ["ASC", "DESC", ] 
**source_column** | str,  | str,  | Source column in the physical database. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | Metadata tags. | [optional] 
**title** | str,  | str,  | Human readable title. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# labels

Attribute labels.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Attribute labels. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**AacLabel**](AacLabel.md) | [**AacLabel**](AacLabel.md) | any string name can be used but the value must be the correct type | [optional] 

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

