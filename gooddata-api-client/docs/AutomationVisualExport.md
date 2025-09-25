# AutomationVisualExport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_payload** | [**VisualExportRequest**](VisualExportRequest.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_visual_export import AutomationVisualExport

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationVisualExport from a JSON string
automation_visual_export_instance = AutomationVisualExport.from_json(json)
# print the JSON string representation of the object
print(AutomationVisualExport.to_json())

# convert the object into a dict
automation_visual_export_dict = automation_visual_export_instance.to_dict()
# create an instance of AutomationVisualExport from a dict
automation_visual_export_from_dict = AutomationVisualExport.from_dict(automation_visual_export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


