# DeclarativeDateDataset

A date dataset.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Date dataset description. | [optional] 
**granularities** | **List[str]** | An array of date granularities. All listed granularities will be available for date dataset. | 
**granularities_formatting** | [**GranularitiesFormatting**](GranularitiesFormatting.md) |  | 
**id** | **str** | Date dataset ID. | 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Date dataset title. | 

## Example

```python
from gooddata_api_client.models.declarative_date_dataset import DeclarativeDateDataset

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDateDataset from a JSON string
declarative_date_dataset_instance = DeclarativeDateDataset.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDateDataset.to_json())

# convert the object into a dict
declarative_date_dataset_dict = declarative_date_dataset_instance.to_dict()
# create an instance of DeclarativeDateDataset from a dict
declarative_date_dataset_from_dict = DeclarativeDateDataset.from_dict(declarative_date_dataset_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


