# JsonApiDatasetOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiDatasetOut**](JsonApiDatasetOut.md) |  | 
**included** | [**List[JsonApiDatasetOutIncludes]**](JsonApiDatasetOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_document import JsonApiDatasetOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutDocument from a JSON string
json_api_dataset_out_document_instance = JsonApiDatasetOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutDocument.to_json())

# convert the object into a dict
json_api_dataset_out_document_dict = json_api_dataset_out_document_instance.to_dict()
# create an instance of JsonApiDatasetOutDocument from a dict
json_api_dataset_out_document_from_dict = JsonApiDatasetOutDocument.from_dict(json_api_dataset_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


