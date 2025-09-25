# JsonApiExportDefinitionOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard** | [**JsonApiAutomationInRelationshipsAnalyticalDashboard**](JsonApiAutomationInRelationshipsAnalyticalDashboard.md) |  | [optional] 
**automation** | [**JsonApiAutomationResultOutRelationshipsAutomation**](JsonApiAutomationResultOutRelationshipsAutomation.md) |  | [optional] 
**created_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 
**modified_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 
**visualization_object** | [**JsonApiExportDefinitionInRelationshipsVisualizationObject**](JsonApiExportDefinitionInRelationshipsVisualizationObject.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_export_definition_out_relationships import JsonApiExportDefinitionOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportDefinitionOutRelationships from a JSON string
json_api_export_definition_out_relationships_instance = JsonApiExportDefinitionOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportDefinitionOutRelationships.to_json())

# convert the object into a dict
json_api_export_definition_out_relationships_dict = json_api_export_definition_out_relationships_instance.to_dict()
# create an instance of JsonApiExportDefinitionOutRelationships from a dict
json_api_export_definition_out_relationships_from_dict = JsonApiExportDefinitionOutRelationships.from_dict(json_api_export_definition_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


