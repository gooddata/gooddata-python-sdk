# AacDashboardFilter

Tab-specific filters.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** | Filter type. | 
**date** | **str** | Date dataset reference. | [optional] 
**display_as** | **str** | Display as label. | [optional] 
**_from** | [**AacDashboardFilterFrom**](AacDashboardFilterFrom.md) |  | [optional] 
**granularity** | **str** | Date granularity. | [optional] 
**metric_filters** | **[str]** | Metric filters for validation. | [optional] 
**mode** | **str** | Filter mode. | [optional] 
**multiselect** | **bool** | Whether multiselect is enabled. | [optional] 
**parents** | [**[JsonNode]**](JsonNode.md) | Parent filter references. | [optional] 
**state** | [**AacFilterState**](AacFilterState.md) |  | [optional] 
**title** | **str** | Filter title. | [optional] 
**to** | [**AacDashboardFilterFrom**](AacDashboardFilterFrom.md) |  | [optional] 
**using** | **str** | Attribute or label to filter by. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


