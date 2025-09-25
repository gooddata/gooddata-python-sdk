# AlertCondition

Alert trigger condition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**comparison** | [**Comparison**](Comparison.md) |  | 
**range** | [**Range**](Range.md) |  | 
**relative** | [**Relative**](Relative.md) |  | 

## Example

```python
from gooddata_api_client.models.alert_condition import AlertCondition

# TODO update the JSON string below
json = "{}"
# create an instance of AlertCondition from a JSON string
alert_condition_instance = AlertCondition.from_json(json)
# print the JSON string representation of the object
print(AlertCondition.to_json())

# convert the object into a dict
alert_condition_dict = alert_condition_instance.to_dict()
# create an instance of AlertCondition from a dict
alert_condition_from_dict = AlertCondition.from_dict(alert_condition_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


