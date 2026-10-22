# JsonApiPublisherDocumentInAttributesContent

Content of the document, validated on write. Missing page and section ids, and the `localIdentifier` of an attribute or date filter, are generated. An invalid value is a 400 whose `path` names the first invalid key, such as `content.pages[0].layout.type`. Maximum supported length is 250000 characters.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute_filter_configs** | [**[PublisherDocumentAttributeFilterConfig]**](PublisherDocumentAttributeFilterConfig.md) |  | [optional] 
**defaults** | [**PublisherDocumentDefaults**](PublisherDocumentDefaults.md) |  | [optional] 
**filters** | [**[PublisherDocumentFilter]**](PublisherDocumentFilter.md) | Document filters, at most one per attribute display form or date dataset. | [optional] 
**format_locale** | **str** | Locale for formatting dates in variables, charts and tables. | [optional] 
**locale** | **str** | Locale of the text the product writes, such as &#x60;de-DE&#x60;. | [optional] 
**pages** | [**[PublisherDocumentPage]**](PublisherDocumentPage.md) | The document&#39;s pages, when it has no sections. | [optional] 
**sections** | [**[PublisherDocumentSection]**](PublisherDocumentSection.md) | Groups of pages, when the document has no top-level pages. | [optional] 
**style** | [**PublisherDocumentAreaStyle**](PublisherDocumentAreaStyle.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


