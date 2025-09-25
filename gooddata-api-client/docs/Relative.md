# Relative


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**measure** | [**ArithmeticMeasure**](ArithmeticMeasure.md) |  | 
**operator** | **str** | Relative condition operator. INCREASES_BY - the metric increases by the specified value. DECREASES_BY - the metric decreases by the specified value. CHANGES_BY - the metric increases or decreases by the specified value.  | 
**threshold** | [**Value**](Value.md) |  | 

## Example

```python
from gooddata_api_client.models.relative import Relative

# TODO update the JSON string below
json = "{}"
# create an instance of Relative from a JSON string
relative_instance = Relative.from_json(json)
# print the JSON string representation of the object
print(Relative.to_json())

# convert the object into a dict
relative_dict = relative_instance.to_dict()
# create an instance of Relative from a dict
relative_from_dict = Relative.from_dict(relative_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


