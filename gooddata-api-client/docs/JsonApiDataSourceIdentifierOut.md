# JsonApiDataSourceIdentifierOut

JSON:API representation of dataSourceIdentifier entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDataSourceIdentifierOutAttributes**](JsonApiDataSourceIdentifierOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiDataSourceIdentifierOutMeta**](JsonApiDataSourceIdentifierOutMeta.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_data_source_identifier_out import JsonApiDataSourceIdentifierOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourceIdentifierOut from a JSON string
json_api_data_source_identifier_out_instance = JsonApiDataSourceIdentifierOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourceIdentifierOut.to_json())

# convert the object into a dict
json_api_data_source_identifier_out_dict = json_api_data_source_identifier_out_instance.to_dict()
# create an instance of JsonApiDataSourceIdentifierOut from a dict
json_api_data_source_identifier_out_from_dict = JsonApiDataSourceIdentifierOut.from_dict(json_api_data_source_identifier_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


