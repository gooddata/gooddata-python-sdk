# AlertEvaluationRow


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**computed_metric** | [**MetricRecord**](MetricRecord.md) |  | [optional] 
**label_value** | **str** |  | [optional] 
**primary_metric** | [**MetricRecord**](MetricRecord.md) |  | [optional] 
**secondary_metric** | [**MetricRecord**](MetricRecord.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.alert_evaluation_row import AlertEvaluationRow

# TODO update the JSON string below
json = "{}"
# create an instance of AlertEvaluationRow from a JSON string
alert_evaluation_row_instance = AlertEvaluationRow.from_json(json)
# print the JSON string representation of the object
print(AlertEvaluationRow.to_json())

# convert the object into a dict
alert_evaluation_row_dict = alert_evaluation_row_instance.to_dict()
# create an instance of AlertEvaluationRow from a dict
alert_evaluation_row_from_dict = AlertEvaluationRow.from_dict(alert_evaluation_row_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


