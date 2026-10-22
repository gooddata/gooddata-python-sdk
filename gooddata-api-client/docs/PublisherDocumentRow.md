# PublisherDocumentRow

Lays its children out left to right.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**children** | [**[PublisherDocumentLayoutNode]**](PublisherDocumentLayoutNode.md) | Child nodes from left to right, in reading order; an empty list is a spacer. | 
**type** | **str** |  | defaults to "row"
**id** | **str** |  | [optional] 
**locked** | **bool** | Locks the container in the document editor; never checked on write. | [optional] 
**proportion** | **float** | Share of the parent&#39;s main axis, greater than 0. Default 1. | [optional] 
**style** | [**PublisherDocumentContainerStyle**](PublisherDocumentContainerStyle.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


