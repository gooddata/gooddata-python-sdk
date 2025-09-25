# JsonApiExportDefinitionInRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard** | [**JsonApiAutomationInRelationshipsAnalyticalDashboard**](JsonApiAutomationInRelationshipsAnalyticalDashboard.md) |  | [optional] 
**visualization_object** | [**JsonApiExportDefinitionInRelationshipsVisualizationObject**](JsonApiExportDefinitionInRelationshipsVisualizationObject.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_in_relationships import JsonApiExportDefinitionInRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionInRelationships from a JSON string
json_api_export_definition_in_relationships_instance = JsonApiExportDefinitionInRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionInRelationships.to_json())

# convert the object into a dict
json_api_export_definition_in_relationships_dict = json_api_export_definition_in_relationships_instance.to_dict()
# create an instance of JsonApiExportDefinitionInRelationships from a dict
json_api_export_definition_in_relationships_from_dict = JsonApiExportDefinitionInRelationships.from_dict(json_api_export_definition_in_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


