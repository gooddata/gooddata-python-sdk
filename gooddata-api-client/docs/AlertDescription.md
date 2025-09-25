# AlertDescription


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | **str** |  | [optional] 
**condition** | **str** |  | 
**current_values** | [**List[AlertEvaluationRow]**](AlertEvaluationRow.md) |  | [optional] 
**error_message** | **str** |  | [optional] 
**formatted_threshold** | **str** |  | [optional] 
**lower_threshold** | **float** |  | [optional] 
**metric** | **str** |  | 
**remaining_alert_evaluation_count** | **int** |  | [optional] 
**status** | **str** |  | [optional] 
**threshold** | **float** |  | [optional] 
**total_value_count** | **int** |  | [optional] 
**trace_id** | **str** |  | [optional] 
**triggered_at** | **datetime** |  | [optional] 
**triggered_count** | **int** |  | [optional] 
**upper_threshold** | **float** |  | [optional] 

## Example

```python
from gooddata_api_client.models.alert_description import AlertDescription

# TODO update the JSON string below
json = "{}"
# create an instance of AlertDescription from a JSON string
alert_description_instance = AlertDescription.from_json(json)
# print the JSON string representation of the object
print(AlertDescription.to_json())

# convert the object into a dict
alert_description_dict = alert_description_instance.to_dict()
# create an instance of AlertDescription from a dict
alert_description_from_dict = AlertDescription.from_dict(alert_description_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


