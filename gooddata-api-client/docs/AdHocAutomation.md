# AdHocAutomation


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**alert** | [**AutomationAlert**](AutomationAlert.md) |  | [optional] 
**analytical_dashboard** | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) |  | [optional] 
**dashboard_tabular_exports** | [**List[AutomationDashboardTabularExport]**](AutomationDashboardTabularExport.md) |  | [optional] 
**description** | **str** |  | [optional] 
**details** | **Dict[str, str]** | Additional details to be included in the automated message. | [optional] 
**external_recipients** | [**List[AutomationExternalRecipient]**](AutomationExternalRecipient.md) | External recipients of the automation action results. | [optional] 
**image_exports** | [**List[AutomationImageExport]**](AutomationImageExport.md) |  | [optional] 
**metadata** | [**AutomationMetadata**](AutomationMetadata.md) |  | [optional] 
**notification_channel** | [**DeclarativeNotificationChannelIdentifier**](DeclarativeNotificationChannelIdentifier.md) |  | [optional] 
**raw_exports** | [**List[AutomationRawExport]**](AutomationRawExport.md) |  | [optional] 
**recipients** | [**List[DeclarativeUserIdentifier]**](DeclarativeUserIdentifier.md) |  | [optional] 
**slides_exports** | [**List[AutomationSlidesExport]**](AutomationSlidesExport.md) |  | [optional] 
**tabular_exports** | [**List[AutomationTabularExport]**](AutomationTabularExport.md) |  | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** |  | [optional] 
**visual_exports** | [**List[AutomationVisualExport]**](AutomationVisualExport.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.ad_hoc_automation import AdHocAutomation

# TODO update the JSON string below
json = "{}"
# create an instance of AdHocAutomation from a JSON string
ad_hoc_automation_instance = AdHocAutomation.from_json(json)
# print the JSON string representation of the object
print(AdHocAutomation.to_json())

# convert the object into a dict
ad_hoc_automation_dict = ad_hoc_automation_instance.to_dict()
# create an instance of AdHocAutomation from a dict
ad_hoc_automation_from_dict = AdHocAutomation.from_dict(ad_hoc_automation_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


