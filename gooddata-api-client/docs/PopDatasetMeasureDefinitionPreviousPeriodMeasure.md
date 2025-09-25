# PopDatasetMeasureDefinitionPreviousPeriodMeasure


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**date_datasets** | [**List[PopDataset]**](PopDataset.md) | Specification of which date data sets to use for determining the period to calculate the previous period for. | 
**measure_identifier** | [**AfmLocalIdentifier**](AfmLocalIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.pop_dataset_measure_definition_previous_period_measure import PopDatasetMeasureDefinitionPreviousPeriodMeasure

# TODO update the JSON string below
json = "{}"
# create an instance of PopDatasetMeasureDefinitionPreviousPeriodMeasure from a JSON string
pop_dataset_measure_definition_previous_period_measure_instance = PopDatasetMeasureDefinitionPreviousPeriodMeasure.from_json(json)
# print the JSON string representation of the object
print(PopDatasetMeasureDefinitionPreviousPeriodMeasure.to_json())

# convert the object into a dict
pop_dataset_measure_definition_previous_period_measure_dict = pop_dataset_measure_definition_previous_period_measure_instance.to_dict()
# create an instance of PopDatasetMeasureDefinitionPreviousPeriodMeasure from a dict
pop_dataset_measure_definition_previous_period_measure_from_dict = PopDatasetMeasureDefinitionPreviousPeriodMeasure.from_dict(pop_dataset_measure_definition_previous_period_measure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


