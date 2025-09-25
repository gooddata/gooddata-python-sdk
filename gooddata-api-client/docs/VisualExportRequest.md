# VisualExportRequest

Export request object describing the export properties and metadata for dashboard PDF exports.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_id** | **str** | Dashboard identifier | 
**file_name** | **str** | File name to be used for retrieving the pdf document. | 
**metadata** | **object** | Metadata definition in free-form JSON format. | [optional] 

## Example

```python
from gooddata_api_client.models.visual_export_request import VisualExportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of VisualExportRequest from a JSON string
visual_export_request_instance = VisualExportRequest.from_json(json)
# print the JSON string representation of the object
print(VisualExportRequest.to_json())

# convert the object into a dict
visual_export_request_dict = visual_export_request_instance.to_dict()
# create an instance of VisualExportRequest from a dict
visual_export_request_from_dict = VisualExportRequest.from_dict(visual_export_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


