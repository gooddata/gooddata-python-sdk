# PdfTableStyleProperty

CSS property.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**key** | **str** | CSS property key. | 
**value** | **str** | CSS property value. | 

## Example

```python
from gooddata_api_client.models.pdf_table_style_property import PdfTableStyleProperty

# TODO update the JSON string below
json = "{}"
# create an instance of PdfTableStyleProperty from a JSON string
pdf_table_style_property_instance = PdfTableStyleProperty.from_json(json)
# print the JSON string representation of the object
print(PdfTableStyleProperty.to_json())

# convert the object into a dict
pdf_table_style_property_dict = pdf_table_style_property_instance.to_dict()
# create an instance of PdfTableStyleProperty from a dict
pdf_table_style_property_from_dict = PdfTableStyleProperty.from_dict(pdf_table_style_property_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


