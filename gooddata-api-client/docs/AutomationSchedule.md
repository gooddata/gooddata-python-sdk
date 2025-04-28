# AutomationSchedule


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cron** | **str** | Cron expression defining the schedule of the automation. The format is SECOND MINUTE HOUR DAY-OF-MONTH MONTH DAY-OF-WEEK (YEAR). The example expression signifies an action every 30 minutes from 9:00 to 17:00 on workdays. | 
**timezone** | **str** | Timezone in which the schedule is defined. | 
**cron_description** | **str** | Human-readable description of the cron expression. | [optional] [readonly] 
**first_run** | **datetime** | Timestamp of the first scheduled action. If not provided default to the next scheduled time. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


