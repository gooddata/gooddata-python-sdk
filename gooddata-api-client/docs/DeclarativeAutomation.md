# DeclarativeAutomation


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**alert** | [**AutomationAlert**](AutomationAlert.md) |  | [optional] 
**analytical_dashboard** | [**DeclarativeAnalyticalDashboardIdentifier**](DeclarativeAnalyticalDashboardIdentifier.md) |  | [optional] 
**created_at** | **str, none_type** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** |  | [optional] 
**details** | **{str: (str,)}** | TODO | [optional] 
**export_definitions** | [**[DeclarativeExportDefinitionIdentifier]**](DeclarativeExportDefinitionIdentifier.md) |  | [optional] 
**external_recipients** | [**[AutomationExternalRecipient]**](AutomationExternalRecipient.md) | External recipients of the automation action results. | [optional] 
**image_exports** | [**[AutomationImageExport]**](AutomationImageExport.md) |  | [optional] 
**metadata** | [**AutomationMetadata**](AutomationMetadata.md) |  | [optional] 
**modified_at** | **str, none_type** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**notification_channel** | [**DeclarativeNotificationChannelIdentifier**](DeclarativeNotificationChannelIdentifier.md) |  | [optional] 
**recipients** | [**[DeclarativeUserIdentifier]**](DeclarativeUserIdentifier.md) |  | [optional] 
**schedule** | [**AutomationSchedule**](AutomationSchedule.md) |  | [optional] 
**state** | **str** | Current state of the automation. | [optional]  if omitted the server will use the default value of "ACTIVE"
**tabular_exports** | [**[AutomationTabularExport]**](AutomationTabularExport.md) |  | [optional] 
**tags** | **[str]** |  | [optional] 
**title** | **str** |  | [optional] 
**visual_exports** | [**[AutomationVisualExport]**](AutomationVisualExport.md) |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


