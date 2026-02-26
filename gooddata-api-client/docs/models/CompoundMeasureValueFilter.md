# gooddata_api_client.model.compound_measure_value_filter.CompoundMeasureValueFilter

Filter the result by applying multiple comparison and/or range conditions combined with OR logic. If conditions list is empty, no filtering is applied (all rows are returned).

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Filter the result by applying multiple comparison and/or range conditions combined with OR logic. If conditions list is empty, no filtering is applied (all rows are returned). | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[compoundMeasureValueFilter](#compoundMeasureValueFilter)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# compoundMeasureValueFilter

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**measure** | [**AfmIdentifier**](AfmIdentifier.md) | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**[conditions](#conditions)** | list, tuple,  | tuple,  | List of conditions to apply. Conditions are combined with OR logic. Each condition can be either a comparison (e.g., &gt; 100) or a range (e.g., BETWEEN 10 AND 50). If empty, no filtering is applied and all rows are returned. | 
**applyOnResult** | bool,  | BoolClass,  |  | [optional] 
**[dimensionality](#dimensionality)** | list, tuple,  | tuple,  | References to the attributes to be used when filtering. | [optional] 
**localIdentifier** | str,  | str,  |  | [optional] 
**treatNullValuesAs** | decimal.Decimal, int, float,  | decimal.Decimal,  | A value that will be substituted for null values in the metric for the comparisons. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# conditions

List of conditions to apply. Conditions are combined with OR logic. Each condition can be either a comparison (e.g., > 100) or a range (e.g., BETWEEN 10 AND 50). If empty, no filtering is applied and all rows are returned.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of conditions to apply. Conditions are combined with OR logic. Each condition can be either a comparison (e.g., &gt; 100) or a range (e.g., BETWEEN 10 AND 50). If empty, no filtering is applied and all rows are returned. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**MeasureValueCondition**](MeasureValueCondition.md) | [**MeasureValueCondition**](MeasureValueCondition.md) | [**MeasureValueCondition**](MeasureValueCondition.md) |  | 

# dimensionality

References to the attributes to be used when filtering.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | References to the attributes to be used when filtering. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AfmIdentifier**](AfmIdentifier.md) | [**AfmIdentifier**](AfmIdentifier.md) | [**AfmIdentifier**](AfmIdentifier.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

