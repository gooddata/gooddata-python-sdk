# DeclarativeSetting

Setting and its value.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | [optional] 
**id** | **str** | Setting ID. | 
**type** | **str** | Type of the setting. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_setting import DeclarativeSetting

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeSetting from a JSON string
declarative_setting_instance = DeclarativeSetting.from_json(json)
# print the JSON string representation of the object
print(DeclarativeSetting.to_json())

# convert the object into a dict
declarative_setting_dict = declarative_setting_instance.to_dict()
# create an instance of DeclarativeSetting from a dict
declarative_setting_from_dict = DeclarativeSetting.from_dict(declarative_setting_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


