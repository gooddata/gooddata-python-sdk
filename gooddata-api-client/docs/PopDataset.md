# PopDataset

Combination of the date data set to use and how many periods ago to calculate the previous period for.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**AfmObjectIdentifierDataset**](AfmObjectIdentifierDataset.md) |  | 
**periods_ago** | **int** | Number of periods ago to calculate the previous period for. | 

## Example

```python
from gooddata_api_client.models.pop_dataset import PopDataset

# TODO update the JSON string below
json = "{}"
# create an instance of PopDataset from a JSON string
pop_dataset_instance = PopDataset.from_json(json)
# print the JSON string representation of the object
print(PopDataset.to_json())

# convert the object into a dict
pop_dataset_dict = pop_dataset_instance.to_dict()
# create an instance of PopDataset from a dict
pop_dataset_from_dict = PopDataset.from_dict(pop_dataset_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


