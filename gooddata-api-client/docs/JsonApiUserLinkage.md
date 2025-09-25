# JsonApiUserLinkage

The \\\"type\\\" and \\\"id\\\" to non-empty members.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.json_api_user_linkage import JsonApiUserLinkage

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserLinkage from a JSON string
json_api_user_linkage_instance = JsonApiUserLinkage.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserLinkage.to_json())

# convert the object into a dict
json_api_user_linkage_dict = json_api_user_linkage_instance.to_dict()
# create an instance of JsonApiUserLinkage from a dict
json_api_user_linkage_from_dict = JsonApiUserLinkage.from_dict(json_api_user_linkage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


