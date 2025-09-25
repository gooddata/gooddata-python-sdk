# DeclarativeReference

A dataset reference.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**identifier** | [**ReferenceIdentifier**](ReferenceIdentifier.md) |  | 
**multivalue** | **bool** | The multi-value flag enables many-to-many cardinality for references. | 
**source_column_data_types** | **List[str]** | An array of source column data types for a given reference. Deprecated, use &#39;sources&#39; instead. | [optional] 
**source_columns** | **List[str]** | An array of source column names for a given reference. Deprecated, use &#39;sources&#39; instead. | [optional] 
**sources** | [**List[DeclarativeReferenceSource]**](DeclarativeReferenceSource.md) | An array of source columns for a given reference. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_reference import DeclarativeReference

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeReference from a JSON string
declarative_reference_instance = DeclarativeReference.from_json(json)
# print the JSON string representation of the object
print(DeclarativeReference.to_json())

# convert the object into a dict
declarative_reference_dict = declarative_reference_instance.to_dict()
# create an instance of DeclarativeReference from a dict
declarative_reference_from_dict = DeclarativeReference.from_dict(declarative_reference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


