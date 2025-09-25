# JsonApiDataSourceInDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiDataSourceIn**](JsonApiDataSourceIn.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_data_source_in_document import JsonApiDataSourceInDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourceInDocument from a JSON string
json_api_data_source_in_document_instance = JsonApiDataSourceInDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourceInDocument.to_json())

# convert the object into a dict
json_api_data_source_in_document_dict = json_api_data_source_in_document_instance.to_dict()
# create an instance of JsonApiDataSourceInDocument from a dict
json_api_data_source_in_document_from_dict = JsonApiDataSourceInDocument.from_dict(json_api_data_source_in_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


