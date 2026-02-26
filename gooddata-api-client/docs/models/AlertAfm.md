# gooddata_api_client.model.alert_afm.AlertAfm

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[measures](#measures)** | list, tuple,  | tuple,  | Metrics to be computed. One metric if the alert condition is evaluated to a scalar. Two metrics when they should be evaluated to each other. | 
**[filters](#filters)** | list, tuple,  | tuple,  | Various filter types to filter execution result. For anomaly detection, exactly one dataset is specified in the condition. The AFM may contain multiple date filters for different datasets, but only the date filter matching the dataset from the condition is used for anomaly detection. | 
**[attributes](#attributes)** | list, tuple,  | tuple,  | Attributes to be used in the computation. | [optional] 
**[auxMeasures](#auxMeasures)** | list, tuple,  | tuple,  | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# filters

Various filter types to filter execution result. For anomaly detection, exactly one dataset is specified in the condition. The AFM may contain multiple date filters for different datasets, but only the date filter matching the dataset from the condition is used for anomaly detection.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Various filter types to filter execution result. For anomaly detection, exactly one dataset is specified in the condition. The AFM may contain multiple date filters for different datasets, but only the date filter matching the dataset from the condition is used for anomaly detection. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**FilterDefinition**](FilterDefinition.md) | [**FilterDefinition**](FilterDefinition.md) | [**FilterDefinition**](FilterDefinition.md) |  | 

# measures

Metrics to be computed. One metric if the alert condition is evaluated to a scalar. Two metrics when they should be evaluated to each other.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Metrics to be computed. One metric if the alert condition is evaluated to a scalar. Two metrics when they should be evaluated to each other. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 

# attributes

Attributes to be used in the computation.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Attributes to be used in the computation. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) | [**AttributeItem**](AttributeItem.md) |  | 

# auxMeasures

Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) | [**MeasureItem**](MeasureItem.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

