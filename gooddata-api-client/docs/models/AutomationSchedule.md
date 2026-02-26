# gooddata_api_client.model.automation_schedule.AutomationSchedule

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**cron** | str,  | str,  | Cron expression defining the schedule of the automation. The format is SECOND MINUTE HOUR DAY-OF-MONTH MONTH DAY-OF-WEEK (YEAR). The example expression signifies an action every 30 minutes from 9:00 to 17:00 on workdays. | 
**timezone** | str,  | str,  | Timezone in which the schedule is defined. | 
**cronDescription** | str,  | str,  | Human-readable description of the cron expression. | [optional] 
**firstRun** | str, datetime,  | str,  | Timestamp of the first scheduled action. If not provided default to the next scheduled time. | [optional] value must conform to RFC-3339 date-time
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

