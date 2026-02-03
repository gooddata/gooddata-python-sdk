# AacContainerWidget


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**sections** | [**[AacSection]**](AacSection.md) | Nested sections for layout widgets. | 
**additional_properties** | [**{str: (JsonNode,)}**](JsonNode.md) |  | [optional] 
**columns** | **int** | Widget width in grid columns (GAAC). | [optional] 
**container** | **str** | Container widget identifier. | [optional] 
**content** | **str** | Rich text content. | [optional] 
**date** | **str** | Date dataset for filtering. | [optional] 
**description** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**drill_down** | [**JsonNode**](JsonNode.md) |  | [optional] 
**enable_section_headers** | **bool** | Whether section headers are enabled for container widgets. | [optional] 
**ignore_dashboard_filters** | **[str]** | Deprecated. Use ignoredFilters instead. | [optional] 
**ignored_filters** | **[str]** | A list of dashboard filters to be ignored for this widget (GAAC). | [optional] 
**interactions** | [**[JsonNode]**](JsonNode.md) | Widget interactions (GAAC). | [optional] 
**layout_direction** | **str** | Layout direction for container widgets. | [optional] 
**metric** | **str** | Inline metric reference. | [optional] 
**rows** | **int** | Widget height in grid rows (GAAC). | [optional] 
**size** | [**AacWidgetSize**](AacWidgetSize.md) |  | [optional] 
**title** | **bool, date, datetime, dict, float, int, list, str, none_type** |  | [optional] 
**type** | **str** | Widget type. | [optional] 
**visualization** | **str** | Visualization ID reference. | [optional] 
**visualizations** | [**[AacWidget]**](AacWidget.md) | Visualization switcher items. | [optional] 
**zoom_data** | **bool** | Enable zooming to the data for certain visualization types (GAAC). | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


