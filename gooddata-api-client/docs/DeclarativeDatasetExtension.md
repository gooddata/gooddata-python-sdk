# DeclarativeDatasetExtension

A dataset extension properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | The Dataset ID. This ID is further used to refer to this instance of dataset. | 
**workspace_data_filter_references** | [**List[DeclarativeWorkspaceDataFilterReferences]**](DeclarativeWorkspaceDataFilterReferences.md) | An array of explicit workspace data filters. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_dataset_extension import DeclarativeDatasetExtension

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDatasetExtension from a JSON string
declarative_dataset_extension_instance = DeclarativeDatasetExtension.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDatasetExtension.to_json())

# convert the object into a dict
declarative_dataset_extension_dict = declarative_dataset_extension_instance.to_dict()
# create an instance of DeclarativeDatasetExtension from a dict
declarative_dataset_extension_from_dict = DeclarativeDatasetExtension.from_dict(declarative_dataset_extension_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


