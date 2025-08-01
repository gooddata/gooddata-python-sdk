# Settings

Additional settings.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**export_info** | **bool** | Include export info sheet in the exported file. Works only with &#x60;visualizationObject&#x60;. (XLSX) | [optional]  if omitted the server will use the default value of False
**merge_headers** | **bool** | Merge equal headers in neighbouring cells. (XLSX) | [optional] 
**pdf_page_size** | **str** | Page size and orientation. (PDF) | [optional] 
**pdf_table_style** | [**[PdfTableStyle]**](PdfTableStyle.md) | Custom CSS styles for the table. (PDF, HTML) | [optional] 
**pdf_top_left_content** | **str** | Top left header content. (PDF) | [optional] 
**pdf_top_right_content** | **str** | Top right header content. (PDF) | [optional] 
**show_filters** | **bool** | Print applied filters on top of the document. (PDF/HTML when visualizationObject is given) | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


