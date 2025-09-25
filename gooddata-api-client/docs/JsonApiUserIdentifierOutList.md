# JsonApiUserIdentifierOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiUserIdentifierOutWithLinks]**](JsonApiUserIdentifierOutWithLinks.md) |  | 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_identifier_out_list import JsonApiUserIdentifierOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserIdentifierOutList from a JSON string
json_api_user_identifier_out_list_instance = JsonApiUserIdentifierOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserIdentifierOutList.to_json())

# convert the object into a dict
json_api_user_identifier_out_list_dict = json_api_user_identifier_out_list_instance.to_dict()
# create an instance of JsonApiUserIdentifierOutList from a dict
json_api_user_identifier_out_list_from_dict = JsonApiUserIdentifierOutList.from_dict(json_api_user_identifier_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


