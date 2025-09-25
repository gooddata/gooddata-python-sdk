# DatasetReferenceIdentifier


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.dataset_reference_identifier import DatasetReferenceIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DatasetReferenceIdentifier from a JSON string
dataset_reference_identifier_instance = DatasetReferenceIdentifier.from_json(json)
# print the JSON string representation of the object
print(DatasetReferenceIdentifier.to_json())

# convert the object into a dict
dataset_reference_identifier_dict = dataset_reference_identifier_instance.to_dict()
# create an instance of DatasetReferenceIdentifier from a dict
dataset_reference_identifier_from_dict = DatasetReferenceIdentifier.from_dict(dataset_reference_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


