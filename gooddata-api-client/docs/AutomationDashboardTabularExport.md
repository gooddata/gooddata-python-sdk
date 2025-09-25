# AutomationDashboardTabularExport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_payload** | [**DashboardTabularExportRequestV2**](DashboardTabularExportRequestV2.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_dashboard_tabular_export import AutomationDashboardTabularExport

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationDashboardTabularExport from a JSON string
automation_dashboard_tabular_export_instance = AutomationDashboardTabularExport.from_json(json)
# print the JSON string representation of the object
print(AutomationDashboardTabularExport.to_json())

# convert the object into a dict
automation_dashboard_tabular_export_dict = automation_dashboard_tabular_export_instance.to_dict()
# create an instance of AutomationDashboardTabularExport from a dict
automation_dashboard_tabular_export_from_dict = AutomationDashboardTabularExport.from_dict(automation_dashboard_tabular_export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


