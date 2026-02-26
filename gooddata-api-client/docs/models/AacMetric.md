# gooddata_api_client.model.aac_metric.AacMetric

AAC metric definition.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC metric definition. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**id** | str,  | str,  | Unique identifier of the metric. | 
**maql** | str,  | str,  | MAQL expression defining the metric. | 
**type** | str,  | str,  | Metric type discriminator. | 
**description** | str,  | str,  | Metric description. | [optional] 
**format** | str,  | str,  | Default format for metric values. | [optional] 
**is_hidden** | bool,  | BoolClass,  | Deprecated. Use showInAiResults instead. | [optional] 
**is_hidden_from_kda** | bool,  | BoolClass,  | Whether to hide from key driver analysis. | [optional] 
**show_in_ai_results** | bool,  | BoolClass,  | Whether to show in AI results. | [optional] 
**[tags](#tags)** | list, tuple,  | tuple,  | Metadata tags. | [optional] 
**title** | str,  | str,  | Human readable title. | [optional] 
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

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

