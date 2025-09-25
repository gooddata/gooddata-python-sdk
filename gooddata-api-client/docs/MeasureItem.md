# MeasureItem

Metric is a quantity that is calculated from the data.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**definition** | [**MeasureItemDefinition**](MeasureItemDefinition.md) |  | 
**local_identifier** | **str** | Local identifier of the metric. This can be used to reference the metric in other parts of the execution definition. | 

## Example

```python
from gooddata_api_client.models.measure_item import MeasureItem

# TODO update the JSON string below
json = "{}"
# create an instance of MeasureItem from a JSON string
measure_item_instance = MeasureItem.from_json(json)
# print the JSON string representation of the object
print(MeasureItem.to_json())

# convert the object into a dict
measure_item_dict = measure_item_instance.to_dict()
# create an instance of MeasureItem from a dict
measure_item_from_dict = MeasureItem.from_dict(measure_item_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


