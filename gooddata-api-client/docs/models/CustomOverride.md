# gooddata_api_client.model.custom_override.CustomOverride

Custom cell value overrides (IDs will be replaced with specified values).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom cell value overrides (IDs will be replaced with specified values). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[labels](#labels)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomLabels with keys used as placeholders in document. | [optional] 
**[metrics](#metrics)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomMetrics with keys used as placeholders in document. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# labels

Map of CustomLabels with keys used as placeholders in document.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomLabels with keys used as placeholders in document. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**CustomLabel**](CustomLabel.md) | [**CustomLabel**](CustomLabel.md) | any string name can be used but the value must be the correct type | [optional] 

# metrics

Map of CustomMetrics with keys used as placeholders in document.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Map of CustomMetrics with keys used as placeholders in document. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**any_string_name** | [**CustomMetric**](CustomMetric.md) | [**CustomMetric**](CustomMetric.md) | any string name can be used but the value must be the correct type | [optional] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

