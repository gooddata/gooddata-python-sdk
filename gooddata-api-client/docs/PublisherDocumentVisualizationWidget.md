# PublisherDocumentVisualizationWidget

A saved visualization.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique within the page. | 
**type** | **str** |  | defaults to "visualization"
**alt_text** | **str** | Defaults to the visualization&#39;s description. | [optional] 
**date_data_set** | [**PublisherDocumentDataSetRef**](PublisherDocumentDataSetRef.md) |  | [optional] 
**display** | [**PublisherDocumentVisualizationDisplay**](PublisherDocumentVisualizationDisplay.md) |  | [optional] 
**filters** | [**[PublisherDocumentFilter]**](PublisherDocumentFilter.md) | Widget filters; stored, not applied. | [optional] 
**ignore_document_filters** | [**[PublisherDocumentFilterReference]**](PublisherDocumentFilterReference.md) | Document filters this widget ignores. | [optional] 
**ignore_document_period** | **bool** |  | [optional] 
**locked** | **bool** | Locks the widget in the document editor; never checked on write. | [optional] 
**placeholder** | [**PublisherDocumentWidgetPlaceholder**](PublisherDocumentWidgetPlaceholder.md) |  | [optional] 
**proportion** | **float** |  | [optional] 
**style** | [**PublisherDocumentVisualizationStyle**](PublisherDocumentVisualizationStyle.md) |  | [optional] 
**title** | [**PublisherDocumentWidgetTitle**](PublisherDocumentWidgetTitle.md) |  | [optional] 
**visualization** | [**PublisherDocumentVisualizationRef**](PublisherDocumentVisualizationRef.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


