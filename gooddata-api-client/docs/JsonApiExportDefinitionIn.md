# JsonApiExportDefinitionIn

JSON:API representation of exportDefinition entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiExportDefinitionInAttributes**](JsonApiExportDefinitionInAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**relationships** | [**JsonApiExportDefinitionInRelationships**](JsonApiExportDefinitionInRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_in import JsonApiExportDefinitionIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionIn from a JSON string
json_api_export_definition_in_instance = JsonApiExportDefinitionIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionIn.to_json())

# convert the object into a dict
json_api_export_definition_in_dict = json_api_export_definition_in_instance.to_dict()
# create an instance of JsonApiExportDefinitionIn from a dict
json_api_export_definition_in_from_dict = JsonApiExportDefinitionIn.from_dict(json_api_export_definition_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


