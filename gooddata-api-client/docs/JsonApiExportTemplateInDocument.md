# JsonApiExportTemplateInDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiExportTemplateIn**](JsonApiExportTemplateIn.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_export_template_in_document import JsonApiExportTemplateInDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportTemplateInDocument from a JSON string
json_api_export_template_in_document_instance = JsonApiExportTemplateInDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportTemplateInDocument.to_json())

# convert the object into a dict
json_api_export_template_in_document_dict = json_api_export_template_in_document_instance.to_dict()
# create an instance of JsonApiExportTemplateInDocument from a dict
json_api_export_template_in_document_from_dict = JsonApiExportTemplateInDocument.from_dict(json_api_export_template_in_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


