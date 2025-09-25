# JsonApiExportDefinitionOutAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**are_relations_valid** | **bool** |  | [optional] 
**created_at** | **datetime** |  | [optional] 
**description** | **str** |  | [optional] 
**modified_at** | **datetime** |  | [optional] 
**request_payload** | [**JsonApiExportDefinitionInAttributesRequestPayload**](JsonApiExportDefinitionInAttributesRequestPayload.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_out_attributes import JsonApiExportDefinitionOutAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionOutAttributes from a JSON string
json_api_export_definition_out_attributes_instance = JsonApiExportDefinitionOutAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionOutAttributes.to_json())

# convert the object into a dict
json_api_export_definition_out_attributes_dict = json_api_export_definition_out_attributes_instance.to_dict()
# create an instance of JsonApiExportDefinitionOutAttributes from a dict
json_api_export_definition_out_attributes_from_dict = JsonApiExportDefinitionOutAttributes.from_dict(json_api_export_definition_out_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


