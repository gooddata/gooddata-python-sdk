# AutomationTabularExport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_payload** | [**TabularExportRequest**](TabularExportRequest.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_tabular_export import AutomationTabularExport

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationTabularExport from a JSON string
automation_tabular_export_instance = AutomationTabularExport.from_json(json)
# print the JSON string representation of the object
print(AutomationTabularExport.to_json())

# convert the object into a dict
automation_tabular_export_dict = automation_tabular_export_instance.to_dict()
# create an instance of AutomationTabularExport from a dict
automation_tabular_export_from_dict = AutomationTabularExport.from_dict(automation_tabular_export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


