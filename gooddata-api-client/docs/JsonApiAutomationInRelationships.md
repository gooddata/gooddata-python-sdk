# JsonApiAutomationInRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard** | [**JsonApiAutomationInRelationshipsAnalyticalDashboard**](JsonApiAutomationInRelationshipsAnalyticalDashboard.md) |  | [optional] 
**export_definitions** | [**JsonApiAutomationInRelationshipsExportDefinitions**](JsonApiAutomationInRelationshipsExportDefinitions.md) |  | [optional] 
**notification_channel** | [**JsonApiAutomationInRelationshipsNotificationChannel**](JsonApiAutomationInRelationshipsNotificationChannel.md) |  | [optional] 
**recipients** | [**JsonApiAutomationInRelationshipsRecipients**](JsonApiAutomationInRelationshipsRecipients.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_automation_in_relationships import JsonApiAutomationInRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationInRelationships from a JSON string
json_api_automation_in_relationships_instance = JsonApiAutomationInRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationInRelationships.to_json())

# convert the object into a dict
json_api_automation_in_relationships_dict = json_api_automation_in_relationships_instance.to_dict()
# create an instance of JsonApiAutomationInRelationships from a dict
json_api_automation_in_relationships_from_dict = JsonApiAutomationInRelationships.from_dict(json_api_automation_in_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


