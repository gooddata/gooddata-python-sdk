# gooddata_api_client.model.raw_custom_override.RawCustomOverride

Custom cell value overrides (IDs will be replaced with specified values).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom cell value overrides (IDs will be replaced with specified values). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[labels](#labels)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomLabels with keys used as placeholders in export result. | [optional] 
**[metrics](#metrics)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomMetrics with keys used as placeholders in export result. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# labels

Map of CustomLabels with keys used as placeholders in export result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomLabels with keys used as placeholders in export result. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**RawCustomLabel**](RawCustomLabel.md) | [**RawCustomLabel**](RawCustomLabel.md) | any string name can be used but the value must be the correct type | [optional] 

# metrics

Map of CustomMetrics with keys used as placeholders in export result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomMetrics with keys used as placeholders in export result. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**RawCustomMetric**](RawCustomMetric.md) | [**RawCustomMetric**](RawCustomMetric.md) | any string name can be used but the value must be the correct type | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

