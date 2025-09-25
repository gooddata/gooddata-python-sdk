# JsonApiFactOutRelationships


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dataset** | [**JsonApiAggregatedFactOutRelationshipsDataset**](JsonApiAggregatedFactOutRelationshipsDataset.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_fact_out_relationships import JsonApiFactOutRelationships

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFactOutRelationships from a JSON string
json_api_fact_out_relationships_instance = JsonApiFactOutRelationships.from_json(json)
# print the JSON string representation of the object
print(JsonApiFactOutRelationships.to_json())

# convert the object into a dict
json_api_fact_out_relationships_dict = json_api_fact_out_relationships_instance.to_dict()
# create an instance of JsonApiFactOutRelationships from a dict
json_api_fact_out_relationships_from_dict = JsonApiFactOutRelationships.from_dict(json_api_fact_out_relationships_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


