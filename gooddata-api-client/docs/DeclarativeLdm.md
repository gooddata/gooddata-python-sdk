# DeclarativeLdm

A logical data model (LDM) representation.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset_extensions** | [**List[DeclarativeDatasetExtension]**](DeclarativeDatasetExtension.md) | An array containing extensions for datasets defined in parent workspaces. | [optional] 
**datasets** | [**List[DeclarativeDataset]**](DeclarativeDataset.md) | An array containing datasets. | [optional] 
**date_instances** | [**List[DeclarativeDateDataset]**](DeclarativeDateDataset.md) | An array containing date-related datasets. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_ldm import DeclarativeLdm

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeLdm from a JSON string
declarative_ldm_instance = DeclarativeLdm.from_json(json)
# print the JSON string representation of the object
print(DeclarativeLdm.to_json())

# convert the object into a dict
declarative_ldm_dict = declarative_ldm_instance.to_dict()
# create an instance of DeclarativeLdm from a dict
declarative_ldm_from_dict = DeclarativeLdm.from_dict(declarative_ldm_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


