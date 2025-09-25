# FactIdentifier

A fact identifier.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Fact ID. | 
**type** | **str** | A type of the fact. | 

## Example

```python
from gooddata_api_client.models.fact_identifier import FactIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of FactIdentifier from a JSON string
fact_identifier_instance = FactIdentifier.from_json(json)
# print the JSON string representation of the object
print(FactIdentifier.to_json())

# convert the object into a dict
fact_identifier_dict = fact_identifier_instance.to_dict()
# create an instance of FactIdentifier from a dict
fact_identifier_from_dict = FactIdentifier.from_dict(fact_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


