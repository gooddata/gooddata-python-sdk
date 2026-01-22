# AlertAfm


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**filters** | [**[FilterDefinition]**](FilterDefinition.md) | Various filter types to filter execution result. For anomaly detection, exactly one dataset is specified in the condition. The AFM may contain multiple date filters for different datasets, but only the date filter matching the dataset from the condition is used for anomaly detection. | 
**measures** | [**[MeasureItem]**](MeasureItem.md) | Metrics to be computed. One metric if the alert condition is evaluated to a scalar. Two metrics when they should be evaluated to each other. | 
**attributes** | [**[AttributeItem]**](AttributeItem.md) | Attributes to be used in the computation. | [optional] 
**aux_measures** | [**[MeasureItem]**](MeasureItem.md) | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


