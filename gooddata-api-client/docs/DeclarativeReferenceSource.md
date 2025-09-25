# DeclarativeReferenceSource

A dataset reference source column description.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**column** | **str** | A name of the source column in the table. | 
**data_type** | **str** | A type of the source column. | [optional] 
**target** | [**GrainIdentifier**](GrainIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_reference_source import DeclarativeReferenceSource

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeReferenceSource from a JSON string
declarative_reference_source_instance = DeclarativeReferenceSource.from_json(json)
# print the JSON string representation of the object
print(DeclarativeReferenceSource.to_json())

# convert the object into a dict
declarative_reference_source_dict = declarative_reference_source_instance.to_dict()
# create an instance of DeclarativeReferenceSource from a dict
declarative_reference_source_from_dict = DeclarativeReferenceSource.from_dict(declarative_reference_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


