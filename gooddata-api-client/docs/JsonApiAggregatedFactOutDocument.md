# JsonApiAggregatedFactOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiAggregatedFactOut**](JsonApiAggregatedFactOut.md) |  | 
**included** | [**List[JsonApiAggregatedFactOutIncludes]**](JsonApiAggregatedFactOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_aggregated_fact_out_document import JsonApiAggregatedFactOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAggregatedFactOutDocument from a JSON string
json_api_aggregated_fact_out_document_instance = JsonApiAggregatedFactOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiAggregatedFactOutDocument.to_json())

# convert the object into a dict
json_api_aggregated_fact_out_document_dict = json_api_aggregated_fact_out_document_instance.to_dict()
# create an instance of JsonApiAggregatedFactOutDocument from a dict
json_api_aggregated_fact_out_document_from_dict = JsonApiAggregatedFactOutDocument.from_dict(json_api_aggregated_fact_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


