# ResolvedSetting

Setting and its value.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | [optional] 
**id** | **str** | Setting ID. Formerly used to identify a type of a particular setting, going to be removed in a favor of setting&#39;s type. | 
**type** | **str** | Type of the setting. | [optional] 

## Example

```python
from gooddata_api_client.models.resolved_setting import ResolvedSetting

# TODO update the JSON string below
json = "{}"
# create an instance of ResolvedSetting from a JSON string
resolved_setting_instance = ResolvedSetting.from_json(json)
# print the JSON string representation of the object
print(ResolvedSetting.to_json())

# convert the object into a dict
resolved_setting_dict = resolved_setting_instance.to_dict()
# create an instance of ResolvedSetting from a dict
resolved_setting_from_dict = ResolvedSetting.from_dict(resolved_setting_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


