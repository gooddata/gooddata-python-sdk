# AfmObjectIdentifierDataset

Reference to the date dataset to which the filter should be applied.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**AfmObjectIdentifierDatasetIdentifier**](AfmObjectIdentifierDatasetIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.afm_object_identifier_dataset import AfmObjectIdentifierDataset

# TODO update the JSON string below
json = "{}"
# create an instance of AfmObjectIdentifierDataset from a JSON string
afm_object_identifier_dataset_instance = AfmObjectIdentifierDataset.from_json(json)
# print the JSON string representation of the object
print(AfmObjectIdentifierDataset.to_json())

# convert the object into a dict
afm_object_identifier_dataset_dict = afm_object_identifier_dataset_instance.to_dict()
# create an instance of AfmObjectIdentifierDataset from a dict
afm_object_identifier_dataset_from_dict = AfmObjectIdentifierDataset.from_dict(afm_object_identifier_dataset_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


