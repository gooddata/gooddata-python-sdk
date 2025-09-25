# AlertAfm


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**List[AttributeItem]**](AttributeItem.md) | Attributes to be used in the computation. | [optional] 
**aux_measures** | [**List[MeasureItem]**](MeasureItem.md) | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | [optional] 
**filters** | [**List[FilterDefinition]**](FilterDefinition.md) | Various filter types to filter execution result. | 
**measures** | [**List[MeasureItem]**](MeasureItem.md) | Metrics to be computed. One metric if the alert condition is evaluated to a scalar. Two metrics when they should be evaluated to each other. | 

## Example

```python
from gooddata_api_client.models.alert_afm import AlertAfm

# TODO update the JSON string below
json = "{}"
# create an instance of AlertAfm from a JSON string
alert_afm_instance = AlertAfm.from_json(json)
# print the JSON string representation of the object
print(AlertAfm.to_json())

# convert the object into a dict
alert_afm_dict = alert_afm_instance.to_dict()
# create an instance of AlertAfm from a dict
alert_afm_from_dict = AlertAfm.from_dict(alert_afm_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


