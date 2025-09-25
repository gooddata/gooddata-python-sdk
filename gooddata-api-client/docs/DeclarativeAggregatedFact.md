# DeclarativeAggregatedFact

A dataset fact.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | Fact description. | [optional] 
**id** | **str** | Fact ID. | 
**source_column** | **str** | A name of the source column in the table. | 
**source_column_data_type** | **str** | A type of the source column | [optional] 
**source_fact_reference** | [**DeclarativeSourceFactReference**](DeclarativeSourceFactReference.md) |  | 
**tags** | **List[str]** | A list of tags. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_aggregated_fact import DeclarativeAggregatedFact

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAggregatedFact from a JSON string
declarative_aggregated_fact_instance = DeclarativeAggregatedFact.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAggregatedFact.to_json())

# convert the object into a dict
declarative_aggregated_fact_dict = declarative_aggregated_fact_instance.to_dict()
# create an instance of DeclarativeAggregatedFact from a dict
declarative_aggregated_fact_from_dict = DeclarativeAggregatedFact.from_dict(declarative_aggregated_fact_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


