# JsonApiDataSourceIdentifierOutWithLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDataSourceIdentifierOutAttributes**](JsonApiDataSourceIdentifierOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiDataSourceIdentifierOutMeta**](JsonApiDataSourceIdentifierOutMeta.md) |  | [optional] 
**type** | **str** | Object type | 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_data_source_identifier_out_with_links import JsonApiDataSourceIdentifierOutWithLinks

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourceIdentifierOutWithLinks from a JSON string
json_api_data_source_identifier_out_with_links_instance = JsonApiDataSourceIdentifierOutWithLinks.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourceIdentifierOutWithLinks.to_json())

# convert the object into a dict
json_api_data_source_identifier_out_with_links_dict = json_api_data_source_identifier_out_with_links_instance.to_dict()
# create an instance of JsonApiDataSourceIdentifierOutWithLinks from a dict
json_api_data_source_identifier_out_with_links_from_dict = JsonApiDataSourceIdentifierOutWithLinks.from_dict(json_api_data_source_identifier_out_with_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


