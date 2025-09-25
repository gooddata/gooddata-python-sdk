# SlidesExportRequest

Export request object describing the export properties and metadata for slides exports.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_id** | **str** | Dashboard identifier | [optional] 
**file_name** | **str** | File name to be used for retrieving the pdf document. | 
**format** | **str** | Requested resulting file type. | 
**metadata** | **object** | Free-form JSON object | [optional] 
**template_id** | **str** | Export template identifier. | [optional] 
**visualization_ids** | **List[str]** | List of visualization ids to be exported. Note that only one visualization is currently supported. | [optional] 
**widget_ids** | **List[str]** | List of widget identifiers to be exported. Note that only one widget is currently supported. | [optional] 

## Example

```python
from gooddata_api_client.models.slides_export_request import SlidesExportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SlidesExportRequest from a JSON string
slides_export_request_instance = SlidesExportRequest.from_json(json)
# print the JSON string representation of the object
print(SlidesExportRequest.to_json())

# convert the object into a dict
slides_export_request_dict = slides_export_request_instance.to_dict()
# create an instance of SlidesExportRequest from a dict
slides_export_request_from_dict = SlidesExportRequest.from_dict(slides_export_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


