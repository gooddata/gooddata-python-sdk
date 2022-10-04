# ExecutionResultGrandTotal

Contains the data of grand totals with the same dimensions.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | **[{str: (bool, date, datetime, dict, float, int, list, str, none_type)}]** | A multi-dimensional array of computed results. The most common one being a 2-dimensional array. The arrays can be composed of Double or null values. | 
**dimension_headers** | [**[DimensionHeader]**](DimensionHeader.md) | Contains headers for a subset of &#x60;totalDimensions&#x60; in which the totals are grand totals. | 
**total_dimensions** | **[str]** | Dimensions of the grand totals. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


