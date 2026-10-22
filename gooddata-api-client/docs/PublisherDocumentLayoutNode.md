# PublisherDocumentLayoutNode

A layout node: a row or column container, or a widget. The shape is selected by `type`.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**type** | **str** |  | defaults to "takeaway"
**locked** | **bool** | Locks the widget in the document editor; never checked on write. | [optional] 
**proportion** | **float** |  | [optional] 
**style** | [**PublisherDocumentTextWidgetStyle**](PublisherDocumentTextWidgetStyle.md) |  | [optional] 
**markdown** | **str** | The generated text. | [optional] 
**placeholder** | [**PublisherDocumentWidgetPlaceholder**](PublisherDocumentWidgetPlaceholder.md) |  | [optional] 
**level** | **int** | Outline level below the page title. Default 1. | [optional] 
**decorative** | **bool** | Left out of the accessibility tree, PDF tags and the AI context; needs no alt text. | [optional] 
**alt_text** | **str** | Defaults to the visualization&#39;s description. | [optional] 
**source** | **str** | A theme image reference such as &#x60;{theme.logo}&#x60;, or an &#x60;https://&#x60; URL. | [optional] 
**date_data_set** | [**PublisherDocumentDataSetRef**](PublisherDocumentDataSetRef.md) |  | [optional] 
**display** | [**PublisherDocumentVisualizationDisplay**](PublisherDocumentVisualizationDisplay.md) |  | [optional] 
**filters** | [**[PublisherDocumentFilter]**](PublisherDocumentFilter.md) | Widget filters; stored, not applied. | [optional] 
**ignore_document_filters** | [**[PublisherDocumentFilterReference]**](PublisherDocumentFilterReference.md) | Document filters this widget ignores. | [optional] 
**ignore_document_period** | **bool** |  | [optional] 
**title** | [**PublisherDocumentWidgetTitle**](PublisherDocumentWidgetTitle.md) |  | [optional] 
**visualization** | [**PublisherDocumentVisualizationRef**](PublisherDocumentVisualizationRef.md) |  | [optional] 
**generation** | [**PublisherDocumentTakeawayGeneration**](PublisherDocumentTakeawayGeneration.md) |  | [optional] 
**children** | [**[PublisherDocumentLayoutNode]**](PublisherDocumentLayoutNode.md) | Child nodes from top to bottom, in reading order; an empty list is a spacer. | [optional] 
**id** | **str** | Unique within the page. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


