# RangeMeasureValueFilterBody


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure** | [**Identifier**](Identifier.md) |  | 
**operator** | **str** |  | 
**_from** | **float** |  | 
**to** | **float** |  | 
**apply_on_result** | **bool** | Force the filter to be applied on the result (true) or source data (false). If not specified at all the default behaviour specific to each type of filter is used. | [optional] 
**dimensionality** | [**[Identifier]**](Identifier.md) |  | [optional] 
**treat_null_values_as** | **float** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


