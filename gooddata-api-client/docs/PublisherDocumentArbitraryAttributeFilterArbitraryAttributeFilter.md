# PublisherDocumentArbitraryAttributeFilterArbitraryAttributeFilter


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**display_form** | [**PublisherDocumentObjRef**](PublisherDocumentObjRef.md) |  | 
**negative_selection** | **bool** |  | 
**values** | **[str]** | Values; &#x60;null&#x60; stands for an empty value. | 
**filter_elements_by** | [**[PublisherDocumentAttributeFilterParent]**](PublisherDocumentAttributeFilterParent.md) |  | [optional] 
**filter_elements_by_date** | [**[PublisherDocumentAttributeFilterByDate]**](PublisherDocumentAttributeFilterByDate.md) |  | [optional] 
**local_identifier** | **str** | Required on a document filter in the declarative layout. A REST write can omit it there. The server then generates it. Optional on a page filter. | [optional] 
**title** | **str** |  | [optional] 
**validate_elements_by** | [**[PublisherDocumentObjRef]**](PublisherDocumentObjRef.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


