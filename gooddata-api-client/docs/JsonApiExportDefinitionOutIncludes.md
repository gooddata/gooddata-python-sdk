# JsonApiExportDefinitionOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiUserIdentifierOutAttributes**](JsonApiUserIdentifierOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAutomationOutRelationships**](JsonApiAutomationOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_out_includes import JsonApiExportDefinitionOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionOutIncludes from a JSON string
json_api_export_definition_out_includes_instance = JsonApiExportDefinitionOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionOutIncludes.to_json())

# convert the object into a dict
json_api_export_definition_out_includes_dict = json_api_export_definition_out_includes_instance.to_dict()
# create an instance of JsonApiExportDefinitionOutIncludes from a dict
json_api_export_definition_out_includes_from_dict = JsonApiExportDefinitionOutIncludes.from_dict(json_api_export_definition_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


