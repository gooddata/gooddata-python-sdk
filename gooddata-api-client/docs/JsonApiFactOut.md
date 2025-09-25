# JsonApiFactOut

JSON:API representation of fact entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiFactOutAttributes**](JsonApiFactOutAttributes.md) |  | [optional] 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiAggregatedFactOutMeta**](JsonApiAggregatedFactOutMeta.md) |  | [optional] 
**relationships** | [**JsonApiFactOutRelationships**](JsonApiFactOutRelationships.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_fact_out import JsonApiFactOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiFactOut from a JSON string
json_api_fact_out_instance = JsonApiFactOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiFactOut.to_json())

# convert the object into a dict
json_api_fact_out_dict = json_api_fact_out_instance.to_dict()
# create an instance of JsonApiFactOut from a dict
json_api_fact_out_from_dict = JsonApiFactOut.from_dict(json_api_fact_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


