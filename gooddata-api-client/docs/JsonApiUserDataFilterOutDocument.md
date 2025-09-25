# JsonApiUserDataFilterOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiUserDataFilterOut**](JsonApiUserDataFilterOut.md) |  | 
**included** | [**List[JsonApiUserDataFilterOutIncludes]**](JsonApiUserDataFilterOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_data_filter_out_document import JsonApiUserDataFilterOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserDataFilterOutDocument from a JSON string
json_api_user_data_filter_out_document_instance = JsonApiUserDataFilterOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserDataFilterOutDocument.to_json())

# convert the object into a dict
json_api_user_data_filter_out_document_dict = json_api_user_data_filter_out_document_instance.to_dict()
# create an instance of JsonApiUserDataFilterOutDocument from a dict
json_api_user_data_filter_out_document_from_dict = JsonApiUserDataFilterOutDocument.from_dict(json_api_user_data_filter_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


