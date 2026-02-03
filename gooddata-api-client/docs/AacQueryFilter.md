# AacQueryFilter

Layer filters.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Filter type. | 
**additional_properties** | [**{str: (JsonNode,)}**](JsonNode.md) |  | [optional] 
**attribute** | **str** | Attribute for ranking filter (identifier or localId). | [optional] 
**bottom** | **int** | Bottom N for ranking filter. | [optional] 
**condition** | **str** | Condition for metric value filter. | [optional] 
**dimensionality** | **[str]** | Dimensionality for metric value filter. | [optional] 
**display_as** | **str** | Display as label (attribute filter). | [optional] 
**_from** | [**AacDashboardFilterFrom**](AacDashboardFilterFrom.md) |  | [optional] 
**granularity** | **str** | Date granularity (date filter). | [optional] 
**null_values_as_zero** | **bool** | Null values are treated as zero (metric value filter). | [optional] 
**state** | [**AacFilterState**](AacFilterState.md) |  | [optional] 
**to** | [**AacDashboardFilterFrom**](AacDashboardFilterFrom.md) |  | [optional] 
**top** | **int** | Top N for ranking filter. | [optional] 
**using** | **str** | Reference to attribute/label/date/metric/fact (type-prefixed id). | [optional] 
**value** | **float** | Value for metric value filter. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


