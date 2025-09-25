# JsonApiAutomationOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard** | [**JsonApiAutomationInRelationshipsAnalyticalDashboard**](JsonApiAutomationInRelationshipsAnalyticalDashboard.md) |  | [optional] 
**automation_results** | [**JsonApiAutomationOutRelationshipsAutomationResults**](JsonApiAutomationOutRelationshipsAutomationResults.md) |  | [optional] 
**created_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 
**export_definitions** | [**JsonApiAutomationInRelationshipsExportDefinitions**](JsonApiAutomationInRelationshipsExportDefinitions.md) |  | [optional] 
**modified_by** | [**JsonApiAnalyticalDashboardOutRelationshipsCreatedBy**](JsonApiAnalyticalDashboardOutRelationshipsCreatedBy.md) |  | [optional] 
**notification_channel** | [**JsonApiAutomationInRelationshipsNotificationChannel**](JsonApiAutomationInRelationshipsNotificationChannel.md) |  | [optional] 
**recipients** | [**JsonApiAutomationInRelationshipsRecipients**](JsonApiAutomationInRelationshipsRecipients.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_automation_out_relationships import JsonApiAutomationOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationOutRelationships from a JSON string
json_api_automation_out_relationships_instance = JsonApiAutomationOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationOutRelationships.to_json())

# convert the object into a dict
json_api_automation_out_relationships_dict = json_api_automation_out_relationships_instance.to_dict()
# create an instance of JsonApiAutomationOutRelationships from a dict
json_api_automation_out_relationships_from_dict = JsonApiAutomationOutRelationships.from_dict(json_api_automation_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


