# JsonApiExportDefinitionPatch

JSON:API representation of patching exportDefinition entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiExportDefinitionInAttributes**](JsonApiExportDefinitionInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiExportDefinitionInRelationships**](JsonApiExportDefinitionInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_patch import JsonApiExportDefinitionPatch

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionPatch from a JSON string
json_api_export_definition_patch_instance = JsonApiExportDefinitionPatch.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionPatch.to_json())

# convert the object into a dict
json_api_export_definition_patch_dict = json_api_export_definition_patch_instance.to_dict()
# create an instance of JsonApiExportDefinitionPatch from a dict
json_api_export_definition_patch_from_dict = JsonApiExportDefinitionPatch.from_dict(json_api_export_definition_patch_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


