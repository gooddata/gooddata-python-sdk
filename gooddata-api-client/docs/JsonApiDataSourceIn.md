# JsonApiDataSourceIn

JSON:API representation of dataSource entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiDataSourceInAttributes**](JsonApiDataSourceInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_data_source_in import JsonApiDataSourceIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourceIn from a JSON string
json_api_data_source_in_instance = JsonApiDataSourceIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourceIn.to_json())

# convert the object into a dict
json_api_data_source_in_dict = json_api_data_source_in_instance.to_dict()
# create an instance of JsonApiDataSourceIn from a dict
json_api_data_source_in_from_dict = JsonApiDataSourceIn.from_dict(json_api_data_source_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


