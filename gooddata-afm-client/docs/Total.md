# Total

Definition of a total. There are two types of totals: grand totals and subtotals. Grand total data will be returned in a separate section of the result structure while subtotals are fully integrated into the main result data. The mechanism for this distinction is automatic and it's described in `TotalDimension`

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function** | **str** | Aggregation function to compute the total. | 
**local_identifier** | **str** | Total identification within this request. Used e.g. in sorting by a total. | 
**metric** | **str** | The metric for which the total will be computed | 
**total_dimensions** | [**[TotalDimension]**](TotalDimension.md) |  | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


