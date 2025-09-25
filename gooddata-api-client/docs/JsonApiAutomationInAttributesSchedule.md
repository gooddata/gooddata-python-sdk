# JsonApiAutomationInAttributesSchedule


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cron** | **str** | Cron expression defining the schedule of the automation. The format is SECOND MINUTE HOUR DAY-OF-MONTH MONTH DAY-OF-WEEK (YEAR). The example expression signifies an action every 30 minutes from 9:00 to 17:00 on workdays. | 
**cron_description** | **str** | Human-readable description of the cron expression. | [optional] [readonly] 
**first_run** | **datetime** | Timestamp of the first scheduled action. If not provided default to the next scheduled time. | [optional] 
**timezone** | **str** | Timezone in which the schedule is defined. | 

## Example

```python
from gooddata_api_client.models.json_api_automation_in_attributes_schedule import JsonApiAutomationInAttributesSchedule

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAutomationInAttributesSchedule from a JSON string
json_api_automation_in_attributes_schedule_instance = JsonApiAutomationInAttributesSchedule.from_json(json)
# print the JSON string representation of the object
print(JsonApiAutomationInAttributesSchedule.to_json())

# convert the object into a dict
json_api_automation_in_attributes_schedule_dict = json_api_automation_in_attributes_schedule_instance.to_dict()
# create an instance of JsonApiAutomationInAttributesSchedule from a dict
json_api_automation_in_attributes_schedule_from_dict = JsonApiAutomationInAttributesSchedule.from_dict(json_api_automation_in_attributes_schedule_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


