# JsonApiDataSourceOut

JSON:API representation of dataSource entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDataSourceOutAttributes**](JsonApiDataSourceOutAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**meta** | [**JsonApiDataSourceIdentifierOutMeta**](JsonApiDataSourceIdentifierOutMeta.md) |  | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_data_source_out import JsonApiDataSourceOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourceOut from a JSON string
json_api_data_source_out_instance = JsonApiDataSourceOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourceOut.to_json())

# convert the object into a dict
json_api_data_source_out_dict = json_api_data_source_out_instance.to_dict()
# create an instance of JsonApiDataSourceOut from a dict
json_api_data_source_out_from_dict = JsonApiDataSourceOut.from_dict(json_api_data_source_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


