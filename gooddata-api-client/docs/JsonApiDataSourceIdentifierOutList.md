# JsonApiDataSourceIdentifierOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiDataSourceIdentifierOutWithLinks]**](JsonApiDataSourceIdentifierOutWithLinks.md) |  | 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_data_source_identifier_out_list import JsonApiDataSourceIdentifierOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourceIdentifierOutList from a JSON string
json_api_data_source_identifier_out_list_instance = JsonApiDataSourceIdentifierOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourceIdentifierOutList.to_json())

# convert the object into a dict
json_api_data_source_identifier_out_list_dict = json_api_data_source_identifier_out_list_instance.to_dict()
# create an instance of JsonApiDataSourceIdentifierOutList from a dict
json_api_data_source_identifier_out_list_from_dict = JsonApiDataSourceIdentifierOutList.from_dict(json_api_data_source_identifier_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


