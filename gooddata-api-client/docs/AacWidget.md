# AacWidget

Widgets in the section.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**additional_properties** | [**{str: (JsonNode,)}**](JsonNode.md) |  | [optional] 
**columns** | **int** | Widget width in grid columns (GAAC). | [optional] 
**content** | **str** | Rich text content. | [optional] 
**date** | **str** | Date dataset for filtering. | [optional] 
**description** | [**AacWidgetDescription**](AacWidgetDescription.md) |  | [optional] 
**drill_down** | [**JsonNode**](JsonNode.md) |  | [optional] 
**ignore_dashboard_filters** | **[str]** | Deprecated. Use ignoredFilters instead. | [optional] 
**ignored_filters** | **[str]** | A list of dashboard filters to be ignored for this widget (GAAC). | [optional] 
**interactions** | [**[JsonNode]**](JsonNode.md) | Widget interactions (GAAC). | [optional] 
**metric** | **str** | Inline metric reference. | [optional] 
**rows** | **int** | Widget height in grid rows (GAAC). | [optional] 
**sections** | [**[AacSection]**](AacSection.md) | Nested sections for layout widgets. | [optional] 
**size** | [**AacWidgetSize**](AacWidgetSize.md) |  | [optional] 
**title** | [**AacWidgetDescription**](AacWidgetDescription.md) |  | [optional] 
**type** | **str** | Widget type. | [optional] 
**visualization** | **str** | Visualization ID reference. | [optional] 
**zoom_data** | **bool** | Enable zooming to the data for certain visualization types (GAAC). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


