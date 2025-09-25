# JsonApiExportDefinitionOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiExportDefinitionOut**](JsonApiExportDefinitionOut.md) |  | 
**included** | [**List[JsonApiExportDefinitionOutIncludes]**](JsonApiExportDefinitionOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_out_document import JsonApiExportDefinitionOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionOutDocument from a JSON string
json_api_export_definition_out_document_instance = JsonApiExportDefinitionOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionOutDocument.to_json())

# convert the object into a dict
json_api_export_definition_out_document_dict = json_api_export_definition_out_document_instance.to_dict()
# create an instance of JsonApiExportDefinitionOutDocument from a dict
json_api_export_definition_out_document_from_dict = JsonApiExportDefinitionOutDocument.from_dict(json_api_export_definition_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


