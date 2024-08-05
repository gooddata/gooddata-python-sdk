# DeclarativeAutomation


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**created_at** | **str, none_type** | Time of the entity creation. | [optional] 
**created_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**description** | **str** |  | [optional] 
**details** | **{str: (str,)}** | TODO | [optional] 
**export_definitions** | [**[DeclarativeExportDefinitionIdentifier]**](DeclarativeExportDefinitionIdentifier.md) |  | [optional] 
**metadata** | [**JsonNode**](JsonNode.md) |  | [optional] 
**modified_at** | **str, none_type** | Time of the last entity modification. | [optional] 
**modified_by** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**notification_channel** | [**DeclarativeNotificationChannelIdentifier**](DeclarativeNotificationChannelIdentifier.md) |  | [optional] 
**recipients** | [**[DeclarativeUserIdentifier]**](DeclarativeUserIdentifier.md) |  | [optional] 
**schedule** | [**AutomationSchedule**](AutomationSchedule.md) |  | [optional] 
**tags** | **[str]** | A list of tags. | [optional] 
**title** | **str** |  | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


