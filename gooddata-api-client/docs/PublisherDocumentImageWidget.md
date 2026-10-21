# PublisherDocumentImageWidget

An image from the theme or an https URL.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Unique within the page. | 
**type** | **str** |  | defaults to "image"
**alt_text** | **str** |  | [optional] 
**decorative** | **bool** | Left out of the accessibility tree, PDF tags and the AI context; needs no alt text. | [optional] 
**locked** | **bool** | Locks the widget in the document editor; never checked on write. | [optional] 
**placeholder** | [**PublisherDocumentWidgetPlaceholder**](PublisherDocumentWidgetPlaceholder.md) |  | [optional] 
**proportion** | **float** |  | [optional] 
**source** | **str** | A theme image reference such as &#x60;{theme.logo}&#x60;, or an &#x60;https://&#x60; URL. | [optional] 
**style** | [**PublisherDocumentImageWidgetStyle**](PublisherDocumentImageWidgetStyle.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


