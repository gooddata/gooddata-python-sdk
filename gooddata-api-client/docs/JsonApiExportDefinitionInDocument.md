# JsonApiExportDefinitionInDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiExportDefinitionIn**](JsonApiExportDefinitionIn.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_in_document import JsonApiExportDefinitionInDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionInDocument from a JSON string
json_api_export_definition_in_document_instance = JsonApiExportDefinitionInDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionInDocument.to_json())

# convert the object into a dict
json_api_export_definition_in_document_dict = json_api_export_definition_in_document_instance.to_dict()
# create an instance of JsonApiExportDefinitionInDocument from a dict
json_api_export_definition_in_document_from_dict = JsonApiExportDefinitionInDocument.from_dict(json_api_export_definition_in_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


