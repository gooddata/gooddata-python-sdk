# JsonApiAggregatedFactOut

JSON:API representation of aggregatedFact entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAggregatedFactOutAttributes**](JsonApiAggregatedFactOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAggregatedFactOutRelationships**](JsonApiAggregatedFactOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_aggregated_fact_out import JsonApiAggregatedFactOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAggregatedFactOut from a JSON string
json_api_aggregated_fact_out_instance = JsonApiAggregatedFactOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiAggregatedFactOut.to_json())

# convert the object into a dict
json_api_aggregated_fact_out_dict = json_api_aggregated_fact_out_instance.to_dict()
# create an instance of JsonApiAggregatedFactOut from a dict
json_api_aggregated_fact_out_from_dict = JsonApiAggregatedFactOut.from_dict(json_api_aggregated_fact_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


