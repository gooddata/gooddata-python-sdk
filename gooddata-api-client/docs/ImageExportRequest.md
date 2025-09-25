# ImageExportRequest

Export request object describing the export properties and metadata for image exports.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dashboard_id** | **str** | Dashboard identifier | 
**file_name** | **str** | File name to be used for retrieving the image document. | 
**format** | **str** | Requested resulting file type. | 
**metadata** | **object** | Free-form JSON object | [optional] 
**widget_ids** | **List[str]** | List of widget identifiers to be exported. Note that only one widget is currently supported. | 

## Example

```python
from gooddata_api_client.models.image_export_request import ImageExportRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ImageExportRequest from a JSON string
image_export_request_instance = ImageExportRequest.from_json(json)
# print the JSON string representation of the object
print(ImageExportRequest.to_json())

# convert the object into a dict
image_export_request_dict = image_export_request_instance.to_dict()
# create an instance of ImageExportRequest from a dict
image_export_request_from_dict = ImageExportRequest.from_dict(image_export_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


