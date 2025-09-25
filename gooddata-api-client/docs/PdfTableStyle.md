# PdfTableStyle

Custom CSS styles for the table. (PDF, HTML)

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | [**List[PdfTableStyleProperty]**](PdfTableStyleProperty.md) | List of CSS properties. | [optional] 
**selector** | **str** | CSS selector where to apply given properties. | 

## Example

```python
from gooddata_api_client.models.pdf_table_style import PdfTableStyle

# TODO update the JSON string below
json = "{}"
# create an instance of PdfTableStyle from a JSON string
pdf_table_style_instance = PdfTableStyle.from_json(json)
# print the JSON string representation of the object
print(PdfTableStyle.to_json())

# convert the object into a dict
pdf_table_style_dict = pdf_table_style_instance.to_dict()
# create an instance of PdfTableStyle from a dict
pdf_table_style_from_dict = PdfTableStyle.from_dict(pdf_table_style_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


