# DeclarativeAutomation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alert** | [**AutomationAlert**](AutomationAlert.md) |  | [optional] 
**analytical_dashboard** | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) |  | [optional] 
**created_at** | **str** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**dashboard_tabular_exports** | [**List[AutomationDashboardTabularExport]**](AutomationDashboardTabularExport.md) |  | [optional] 
**description** | **str** |  | [optional] 
**details** | **Dict[str, str]** | TODO | [optional] 
**evaluation_mode** | **str** | Specify automation evaluation mode. | [optional] [default to 'PER_RECIPIENT']
**export_definitions** | [**List[DeclarativeExportDefinitionIdentifier]**](DeclarativeExportDefinitionIdentifier.md) |  | [optional] 
**external_recipients** | [**List[AutomationExternalRecipient]**](AutomationExternalRecipient.md) | External recipients of the automation action results. | [optional] 
**id** | **str** |  | 
**image_exports** | [**List[AutomationImageExport]**](AutomationImageExport.md) |  | [optional] 
**metadata** | [**AutomationMetadata**](AutomationMetadata.md) |  | [optional] 
**modified_at** | **str** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**notification_channel** | [**DeclarativeNotificationChannelIdentifier**](DeclarativeNotificationChannelIdentifier.md) |  | [optional] 
**raw_exports** | [**List[AutomationRawExport]**](AutomationRawExport.md) |  | [optional] 
**recipients** | [**List[DeclarativeUserIdentifier]**](DeclarativeUserIdentifier.md) |  | [optional] 
**schedule** | [**AutomationSchedule**](AutomationSchedule.md) |  | [optional] 
**slides_exports** | [**List[AutomationSlidesExport]**](AutomationSlidesExport.md) |  | [optional] 
**state** | **str** | Current state of the automation. | [optional] [default to 'ACTIVE']
**tabular_exports** | [**List[AutomationTabularExport]**](AutomationTabularExport.md) |  | [optional] 
**tags** | **List[str]** |  | [optional] 
**title** | **str** |  | [optional] 
**visual_exports** | [**List[AutomationVisualExport]**](AutomationVisualExport.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_automation import DeclarativeAutomation

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAutomation from a JSON string
declarative_automation_instance = DeclarativeAutomation.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAutomation.to_json())

# convert the object into a dict
declarative_automation_dict = declarative_automation_instance.to_dict()
# create an instance of DeclarativeAutomation from a dict
declarative_automation_from_dict = DeclarativeAutomation.from_dict(declarative_automation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


