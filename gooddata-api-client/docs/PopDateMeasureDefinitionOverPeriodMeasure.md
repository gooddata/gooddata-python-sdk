# PopDateMeasureDefinitionOverPeriodMeasure


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_attributes** | [**List[PopDate]**](PopDate.md) | Attributes to use for determining the period to calculate the PoP for. | 
**measure_identifier** | [**AfmLocalIdentifier**](AfmLocalIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.pop_date_measure_definition_over_period_measure import PopDateMeasureDefinitionOverPeriodMeasure

# TODO update the JSON string below
json = "{}"
# create an instance of PopDateMeasureDefinitionOverPeriodMeasure from a JSON string
pop_date_measure_definition_over_period_measure_instance = PopDateMeasureDefinitionOverPeriodMeasure.from_json(json)
# print the JSON string representation of the object
print(PopDateMeasureDefinitionOverPeriodMeasure.to_json())

# convert the object into a dict
pop_date_measure_definition_over_period_measure_dict = pop_date_measure_definition_over_period_measure_instance.to_dict()
# create an instance of PopDateMeasureDefinitionOverPeriodMeasure from a dict
pop_date_measure_definition_over_period_measure_from_dict = PopDateMeasureDefinitionOverPeriodMeasure.from_dict(pop_date_measure_definition_over_period_measure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


