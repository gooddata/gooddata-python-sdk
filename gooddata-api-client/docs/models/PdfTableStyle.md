# gooddata_api_client.model.pdf_table_style.PdfTableStyle

Custom CSS styles for the table. (PDF, HTML)

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Custom CSS styles for the table. (PDF, HTML) | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**selector** | str,  | str,  | CSS selector where to apply given properties. | 
**[properties](#properties)** | list, tuple,  | tuple,  | List of CSS properties. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# properties

List of CSS properties.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of CSS properties. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**PdfTableStyleProperty**](PdfTableStyleProperty.md) | [**PdfTableStyleProperty**](PdfTableStyleProperty.md) | [**PdfTableStyleProperty**](PdfTableStyleProperty.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

