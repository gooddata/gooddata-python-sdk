# ExportRequest

JSON content to be used as export request payload for /export/tabular and /export/visual endpoints. 

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_id** | **str** | Dashboard identifier | 
**file_name** | **str** | Filename of downloaded file without extension. | 
**metadata** | **object** | Free-form JSON object | [optional] 
**custom_override** | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**execution_result** | **str** | Execution result identifier. | [optional] 
**format** | **str** | Expected file format. | 
**related_dashboard_id** | **str** | Analytical dashboard identifier. Optional identifier, which informs the system that the export is related to a specific dashboard. | [optional] 
**settings** | [**Settings**](Settings.md) |  | [optional] 
**visualization_object** | **str** | Visualization object identifier. Alternative to executionResult property. | [optional] 
**visualization_object_custom_filters** | **List[object]** | Optional custom filters (as array of IFilter objects defined in UI SDK) to be applied when visualizationObject is given. Those filters override the original filters defined in the visualization. | [optional] 

## Example

```python
from gooddata_api_client.models.export_request import ExportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ExportRequest from a JSON string
export_request_instance = ExportRequest.from_json(json)
# print the JSON string representation of the object
print(ExportRequest.to_json())

# convert the object into a dict
export_request_dict = export_request_instance.to_dict()
# create an instance of ExportRequest from a dict
export_request_from_dict = ExportRequest.from_dict(export_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


