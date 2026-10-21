# PublisherDocumentPageTemplateContent

Content of a page template: one page without `id` and `visible`.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**layout** | [**PublisherDocumentLayoutNode**](PublisherDocumentLayoutNode.md) |  | 
**filters** | [**[PublisherDocumentFilter]**](PublisherDocumentFilter.md) | Page filters; stored, not applied. | [optional] 
**kind** | **str** | Editor hint. | [optional] 
**notes** | **str** | Speaker notes in markdown, never drawn. | [optional] 
**page_size** | **str** |  | [optional]  if omitted the server will use the default value of "widescreen"
**style** | [**PublisherDocumentPageStyle**](PublisherDocumentPageStyle.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


