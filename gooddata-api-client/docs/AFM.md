# AFM

Top level executable entity. Combination of [A]ttributes, [F]ilters & [M]etrics.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**List[AttributeItem]**](AttributeItem.md) | Attributes to be used in the computation. | 
**aux_measures** | [**List[MeasureItem]**](MeasureItem.md) | Metrics to be referenced from other AFM objects (e.g. filters) but not included in the result. | [optional] 
**filters** | [**List[AFMFiltersInner]**](AFMFiltersInner.md) | Various filter types to filter the execution result. | 
**measures** | [**List[MeasureItem]**](MeasureItem.md) | Metrics to be computed. | 

## Example

```python
from gooddata_api_client.models.afm import AFM

# TODO update the JSON string below
json = "{}"
# create an instance of AFM from a JSON string
afm_instance = AFM.from_json(json)
# print the JSON string representation of the object
print(AFM.to_json())

# convert the object into a dict
afm_dict = afm_instance.to_dict()
# create an instance of AFM from a dict
afm_from_dict = AFM.from_dict(afm_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


