# DeclarativeCustomApplicationSetting

Custom application setting and its value.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**application_name** | **str** | The application id | 
**content** | **object** | Free-form JSON object | 
**id** | **str** | Custom Application Setting ID. | 

## Example

```python
from gooddata_api_client.models.declarative_custom_application_setting import DeclarativeCustomApplicationSetting

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeCustomApplicationSetting from a JSON string
declarative_custom_application_setting_instance = DeclarativeCustomApplicationSetting.from_json(json)
# print the JSON string representation of the object
print(DeclarativeCustomApplicationSetting.to_json())

# convert the object into a dict
declarative_custom_application_setting_dict = declarative_custom_application_setting_instance.to_dict()
# create an instance of DeclarativeCustomApplicationSetting from a dict
declarative_custom_application_setting_from_dict = DeclarativeCustomApplicationSetting.from_dict(declarative_custom_application_setting_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


