# JsonApiUserSettingOutList

A JSON:API document with a list of resources

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiUserSettingOutWithLinks]**](JsonApiUserSettingOutWithLinks.md) |  | 
**links** | [**ListLinks**](ListLinks.md) |  | [optional] 
**meta** | [**JsonApiAggregatedFactOutListMeta**](JsonApiAggregatedFactOutListMeta.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_user_setting_out_list import JsonApiUserSettingOutList

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiUserSettingOutList from a JSON string
json_api_user_setting_out_list_instance = JsonApiUserSettingOutList.from_json(json)
# print the JSON string representation of the object
print(JsonApiUserSettingOutList.to_json())

# convert the object into a dict
json_api_user_setting_out_list_dict = json_api_user_setting_out_list_instance.to_dict()
# create an instance of JsonApiUserSettingOutList from a dict
json_api_user_setting_out_list_from_dict = JsonApiUserSettingOutList.from_dict(json_api_user_setting_out_list_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


