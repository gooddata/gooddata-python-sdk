# TabularExportRequest

Export request object describing the export properties and overrides for tabular exports.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_override** | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**execution_result** | **str** | Execution result identifier. | [optional] 
**file_name** | **str** | Filename of downloaded file without extension. | 
**format** | **str** | Expected file format. | 
**metadata** | **object** | Free-form JSON object | [optional] 
**related_dashboard_id** | **str** | Analytical dashboard identifier. Optional identifier, which informs the system that the export is related to a specific dashboard. | [optional] 
**settings** | [**Settings**](Settings.md) |  | [optional] 
**visualization_object** | **str** | Visualization object identifier. Alternative to executionResult property. | [optional] 
**visualization_object_custom_filters** | **List[object]** | Optional custom filters (as array of IFilter objects defined in UI SDK) to be applied when visualizationObject is given. Those filters override the original filters defined in the visualization. | [optional] 

## Example

```python
from gooddata_api_client.models.tabular_export_request import TabularExportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of TabularExportRequest from a JSON string
tabular_export_request_instance = TabularExportRequest.from_json(json)
# print the JSON string representation of the object
print(TabularExportRequest.to_json())

# convert the object into a dict
tabular_export_request_dict = tabular_export_request_instance.to_dict()
# create an instance of TabularExportRequest from a dict
tabular_export_request_from_dict = TabularExportRequest.from_dict(tabular_export_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


