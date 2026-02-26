# gooddata_api_client.model.what_if_scenario_item.WhatIfScenarioItem

Scenarios with alternative measure calculations

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Scenarios with alternative measure calculations | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[adjustments](#adjustments)** | list, tuple,  | tuple,  | Measure adjustments for this scenario | 
**label** | str,  | str,  | Human-readable scenario label | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# adjustments

Measure adjustments for this scenario

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Measure adjustments for this scenario | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**WhatIfMeasureAdjustmentConfig**](WhatIfMeasureAdjustmentConfig.md) | [**WhatIfMeasureAdjustmentConfig**](WhatIfMeasureAdjustmentConfig.md) | [**WhatIfMeasureAdjustmentConfig**](WhatIfMeasureAdjustmentConfig.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

