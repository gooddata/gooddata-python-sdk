# Settings

Additional settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**export_info** | **bool** | If true, the export will contain the information about the export – exported date, filters, etc. Works only with &#x60;visualizationObject&#x60;. (XLSX, PDF) | [optional] [default to False]
**merge_headers** | **bool** | Merge equal headers in neighbouring cells. (XLSX) | [optional] 
**page_orientation** | **str** | Set page orientation. (PDF) | [optional] [default to 'PORTRAIT']
**page_size** | **str** | Set page size. (PDF) | [optional] [default to 'A4']
**pdf_page_size** | **str** | Page size and orientation. (PDF) | [optional] 
**pdf_table_style** | [**List[PdfTableStyle]**](PdfTableStyle.md) | Custom CSS styles for the table. (PDF, HTML) | [optional] 
**pdf_top_left_content** | **str** | Top left header content. (PDF) | [optional] 
**pdf_top_right_content** | **str** | Top right header content. (PDF) | [optional] 
**show_filters** | **bool** | Print applied filters on top of the document. (PDF/HTML when visualizationObject is given) | [optional] 

## Example

```python
from gooddata_api_client.models.settings import Settings

# TODO update the JSON string below
json = "{}"
# create an instance of Settings from a JSON string
settings_instance = Settings.from_json(json)
# print the JSON string representation of the object
print(Settings.to_json())

# convert the object into a dict
settings_dict = settings_instance.to_dict()
# create an instance of Settings from a dict
settings_from_dict = Settings.from_dict(settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


