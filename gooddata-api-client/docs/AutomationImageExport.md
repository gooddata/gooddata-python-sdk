# AutomationImageExport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_payload** | [**ImageExportRequest**](ImageExportRequest.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_image_export import AutomationImageExport

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationImageExport from a JSON string
automation_image_export_instance = AutomationImageExport.from_json(json)
# print the JSON string representation of the object
print(AutomationImageExport.to_json())

# convert the object into a dict
automation_image_export_dict = automation_image_export_instance.to_dict()
# create an instance of AutomationImageExport from a dict
automation_image_export_from_dict = AutomationImageExport.from_dict(automation_image_export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


