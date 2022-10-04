# TotalDimension

A list of dimensions across which the total will be computed. Total headers for only these dimensions will be returned in the result.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimension_identifier** | **str** | An identifier of a dimension for which the total will be computed. | 
**total_dimension_items** | **[str]** | List of dimension items which will be used for total computation. The total is a grand total in this dimension if the list is empty or it includes the first dimension item from the dimension definition, and its data and header will be returned in a separate &#x60;ExecutionResultGrandTotal&#x60; structure. Otherwise, it is a subtotal and the data will be integrated into the main result. | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


