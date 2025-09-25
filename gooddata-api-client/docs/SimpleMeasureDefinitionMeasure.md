# SimpleMeasureDefinitionMeasure


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**aggregation** | **str** | Definition of aggregation type of the metric. | [optional] 
**compute_ratio** | **bool** | If true, compute the percentage of given metric values (broken down by AFM attributes) to the total (not broken down). | [optional] [default to False]
**filters** | [**List[FilterDefinitionForSimpleMeasure]**](FilterDefinitionForSimpleMeasure.md) | Metrics can be filtered by attribute filters with the same interface as ones for global AFM. Note that only one DateFilter is allowed. | [optional] 
**item** | [**AfmObjectIdentifierCore**](AfmObjectIdentifierCore.md) |  | 

## Example

```python
from gooddata_api_client.models.simple_measure_definition_measure import SimpleMeasureDefinitionMeasure

# TODO update the JSON string below
json = "{}"
# create an instance of SimpleMeasureDefinitionMeasure from a JSON string
simple_measure_definition_measure_instance = SimpleMeasureDefinitionMeasure.from_json(json)
# print the JSON string representation of the object
print(SimpleMeasureDefinitionMeasure.to_json())

# convert the object into a dict
simple_measure_definition_measure_dict = simple_measure_definition_measure_instance.to_dict()
# create an instance of SimpleMeasureDefinitionMeasure from a dict
simple_measure_definition_measure_from_dict = SimpleMeasureDefinitionMeasure.from_dict(simple_measure_definition_measure_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


