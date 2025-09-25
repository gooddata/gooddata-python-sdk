# AutomationSlidesExport


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**request_payload** | [**SlidesExportRequest**](SlidesExportRequest.md) |  | 

## Example

```python
from gooddata_api_client.models.automation_slides_export import AutomationSlidesExport

# TODO update the JSON string below
json = "{}"
# create an instance of AutomationSlidesExport from a JSON string
automation_slides_export_instance = AutomationSlidesExport.from_json(json)
# print the JSON string representation of the object
print(AutomationSlidesExport.to_json())

# convert the object into a dict
automation_slides_export_dict = automation_slides_export_instance.to_dict()
# create an instance of AutomationSlidesExport from a dict
automation_slides_export_from_dict = AutomationSlidesExport.from_dict(automation_slides_export_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


