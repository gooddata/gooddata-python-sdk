# gooddata_api_client.model.what_if_scenario_config.WhatIfScenarioConfig

What-if scenario configuration.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | What-if scenario configuration. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**includeBaseline** | bool,  | BoolClass,  | Whether baseline (unmodified) values are included | 
**[scenarios](#scenarios)** | list, tuple,  | tuple,  | Scenarios with alternative measure calculations | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# scenarios

Scenarios with alternative measure calculations

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Scenarios with alternative measure calculations | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**WhatIfScenarioItem**](WhatIfScenarioItem.md) | [**WhatIfScenarioItem**](WhatIfScenarioItem.md) | [**WhatIfScenarioItem**](WhatIfScenarioItem.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

