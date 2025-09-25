# JsonApiDatasetOutRelationshipsAggregatedFacts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiAggregatedFactLinkage]**](JsonApiAggregatedFactLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_relationships_aggregated_facts import JsonApiDatasetOutRelationshipsAggregatedFacts

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutRelationshipsAggregatedFacts from a JSON string
json_api_dataset_out_relationships_aggregated_facts_instance = JsonApiDatasetOutRelationshipsAggregatedFacts.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutRelationshipsAggregatedFacts.to_json())

# convert the object into a dict
json_api_dataset_out_relationships_aggregated_facts_dict = json_api_dataset_out_relationships_aggregated_facts_instance.to_dict()
# create an instance of JsonApiDatasetOutRelationshipsAggregatedFacts from a dict
json_api_dataset_out_relationships_aggregated_facts_from_dict = JsonApiDatasetOutRelationshipsAggregatedFacts.from_dict(json_api_dataset_out_relationships_aggregated_facts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


