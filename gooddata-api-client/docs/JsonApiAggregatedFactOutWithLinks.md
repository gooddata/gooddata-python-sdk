# JsonApiAggregatedFactOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiAggregatedFactOutAttributes**](JsonApiAggregatedFactOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiAggregatedFactOutRelationships**](JsonApiAggregatedFactOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_aggregated_fact_out_with_links import JsonApiAggregatedFactOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAggregatedFactOutWithLinks from a JSON string
json_api_aggregated_fact_out_with_links_instance = JsonApiAggregatedFactOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiAggregatedFactOutWithLinks.to_json())

# convert the object into a dict
json_api_aggregated_fact_out_with_links_dict = json_api_aggregated_fact_out_with_links_instance.to_dict()
# create an instance of JsonApiAggregatedFactOutWithLinks from a dict
json_api_aggregated_fact_out_with_links_from_dict = JsonApiAggregatedFactOutWithLinks.from_dict(json_api_aggregated_fact_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


