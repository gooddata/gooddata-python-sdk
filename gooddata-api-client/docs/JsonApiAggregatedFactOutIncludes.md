# JsonApiAggregatedFactOutIncludes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiFactOutAttributes**](JsonApiFactOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiFactOutRelationships**](JsonApiFactOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_aggregated_fact_out_includes import JsonApiAggregatedFactOutIncludes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAggregatedFactOutIncludes from a JSON string
json_api_aggregated_fact_out_includes_instance = JsonApiAggregatedFactOutIncludes.from_json(json)
# print the JSON string representation of the object
print(JsonApiAggregatedFactOutIncludes.to_json())

# convert the object into a dict
json_api_aggregated_fact_out_includes_dict = json_api_aggregated_fact_out_includes_instance.to_dict()
# create an instance of JsonApiAggregatedFactOutIncludes from a dict
json_api_aggregated_fact_out_includes_from_dict = JsonApiAggregatedFactOutIncludes.from_dict(json_api_aggregated_fact_out_includes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


