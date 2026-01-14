# CompoundMeasureValueFilterCompoundMeasureValueFilter


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**conditions** | [**[MeasureValueCondition]**](MeasureValueCondition.md) | List of conditions to apply. Conditions are combined with OR logic. Each condition can be either a comparison (e.g., &gt; 100) or a range (e.g., BETWEEN 10 AND 50). If empty, no filtering is applied and all rows are returned. | 
**measure** | [**AfmIdentifier**](AfmIdentifier.md) |  | 
**apply_on_result** | **bool** |  | [optional] 
**dimensionality** | [**[AfmIdentifier]**](AfmIdentifier.md) | References to the attributes to be used when filtering. | [optional] 
**local_identifier** | **str** |  | [optional] 
**treat_null_values_as** | **float** | A value that will be substituted for null values in the metric for the comparisons. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


