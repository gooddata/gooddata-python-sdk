# DeclarativeFact

A dataset fact.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Fact description. | [optional] 
**id** | **str** | Fact ID. | 
**is_hidden** | **bool** | If true, this fact is hidden from AI search results. | [optional] 
**source_column** | **str** | A name of the source column in the table. | 
**source_column_data_type** | **str** | A type of the source column | [optional] 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Fact title. | 

## Example

```python
from gooddata_api_client.models.declarative_fact import DeclarativeFact

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeFact from a JSON string
declarative_fact_instance = DeclarativeFact.from_json(json)
# print the JSON string representation of the object
print(DeclarativeFact.to_json())

# convert the object into a dict
declarative_fact_dict = declarative_fact_instance.to_dict()
# create an instance of DeclarativeFact from a dict
declarative_fact_from_dict = DeclarativeFact.from_dict(declarative_fact_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


