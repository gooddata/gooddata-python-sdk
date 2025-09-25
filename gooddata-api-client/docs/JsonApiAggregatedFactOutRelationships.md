# JsonApiAggregatedFactOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**JsonApiAggregatedFactOutRelationshipsDataset**](JsonApiAggregatedFactOutRelationshipsDataset.md) |  | [optional] 
**source_fact** | [**JsonApiAggregatedFactOutRelationshipsSourceFact**](JsonApiAggregatedFactOutRelationshipsSourceFact.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_aggregated_fact_out_relationships import JsonApiAggregatedFactOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAggregatedFactOutRelationships from a JSON string
json_api_aggregated_fact_out_relationships_instance = JsonApiAggregatedFactOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiAggregatedFactOutRelationships.to_json())

# convert the object into a dict
json_api_aggregated_fact_out_relationships_dict = json_api_aggregated_fact_out_relationships_instance.to_dict()
# create an instance of JsonApiAggregatedFactOutRelationships from a dict
json_api_aggregated_fact_out_relationships_from_dict = JsonApiAggregatedFactOutRelationships.from_dict(json_api_aggregated_fact_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


