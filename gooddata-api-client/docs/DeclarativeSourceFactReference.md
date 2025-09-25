# DeclarativeSourceFactReference

Aggregated awareness source fact reference.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**operation** | **str** | Aggregation operation. | 
**reference** | [**FactIdentifier**](FactIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_source_fact_reference import DeclarativeSourceFactReference

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeSourceFactReference from a JSON string
declarative_source_fact_reference_instance = DeclarativeSourceFactReference.from_json(json)
# print the JSON string representation of the object
print(DeclarativeSourceFactReference.to_json())

# convert the object into a dict
declarative_source_fact_reference_dict = declarative_source_fact_reference_instance.to_dict()
# create an instance of DeclarativeSourceFactReference from a dict
declarative_source_fact_reference_from_dict = DeclarativeSourceFactReference.from_dict(declarative_source_fact_reference_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


