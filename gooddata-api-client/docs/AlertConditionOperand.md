# AlertConditionOperand

Operand of the alert condition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**format** | **str** | Metric format. | [optional] [default to '#,##0.00']
**local_identifier** | **str** | Local identifier of the metric to be compared. | 
**title** | **str** | Metric title. | [optional] 
**value** | **float** | Value of the alert threshold to compare the metric to. | 

## Example

```python
from gooddata_api_client.models.alert_condition_operand import AlertConditionOperand

# TODO update the JSON string below
json = "{}"
# create an instance of AlertConditionOperand from a JSON string
alert_condition_operand_instance = AlertConditionOperand.from_json(json)
# print the JSON string representation of the object
print(AlertConditionOperand.to_json())

# convert the object into a dict
alert_condition_operand_dict = alert_condition_operand_instance.to_dict()
# create an instance of AlertConditionOperand from a dict
alert_condition_operand_from_dict = AlertConditionOperand.from_dict(alert_condition_operand_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


