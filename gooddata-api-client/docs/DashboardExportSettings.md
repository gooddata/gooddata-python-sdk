# DashboardExportSettings

Additional settings.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**export_info** | **bool** | If true, the export will contain the information about the export – exported date, dashboard filters, etc. | [optional] [default to False]
**merge_headers** | **bool** | Merge equal headers in neighbouring cells. Used for [XLSX] format only. | [optional] [default to False]
**page_orientation** | **str** | Set page orientation. (PDF) | [optional] [default to 'PORTRAIT']
**page_size** | **str** | Set page size. (PDF) | [optional] [default to 'A4']

## Example

```python
from gooddata_api_client.models.dashboard_export_settings import DashboardExportSettings

# TODO update the JSON string below
json = "{}"
# create an instance of DashboardExportSettings from a JSON string
dashboard_export_settings_instance = DashboardExportSettings.from_json(json)
# print the JSON string representation of the object
print(DashboardExportSettings.to_json())

# convert the object into a dict
dashboard_export_settings_dict = dashboard_export_settings_instance.to_dict()
# create an instance of DashboardExportSettings from a dict
dashboard_export_settings_from_dict = DashboardExportSettings.from_dict(dashboard_export_settings_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


