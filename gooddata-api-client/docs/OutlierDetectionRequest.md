# OutlierDetectionRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**[AttributeItem]**](AttributeItem.md) | Attributes to be used in the computation. | 
**filters** | [**[ChangeAnalysisParamsFiltersInner]**](ChangeAnalysisParamsFiltersInner.md) | Various filter types to filter the execution result. | 
**granularity** | **str** | Date granularity for anomaly detection. Only time-based granularities are supported (HOUR, DAY, WEEK, MONTH, QUARTER, YEAR). | 
**measures** | [**[MeasureItem]**](MeasureItem.md) |  | 
**sensitivity** | **str** | Sensitivity level for outlier detection | 
**aux_measures** | [**[MeasureItem]**](MeasureItem.md) | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


