# DeclarativeExportDefinitionRequestPayload


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**custom_override** | [**CustomOverride**](CustomOverride.md) |  | [optional] 
**execution_result** | **str** | Execution result identifier. | [optional] 
**file_name** | **str** | File name to be used for retrieving the pdf document. | 
**format** | **str** | Expected file format. | 
**metadata** | **object** | Metadata definition in free-form JSON format. | [optional] 
**related_dashboard_id** | **str** | Analytical dashboard identifier. Optional identifier, which informs the system that the export is related to a specific dashboard. | [optional] 
**settings** | [**Settings**](Settings.md) |  | [optional] 
**visualization_object** | **str** | Visualization object identifier. Alternative to executionResult property. | [optional] 
**visualization_object_custom_filters** | **List[object]** | Optional custom filters (as array of IFilter objects defined in UI SDK) to be applied when visualizationObject is given. Those filters override the original filters defined in the visualization. | [optional] 
**dashboard_id** | **str** | Dashboard identifier | 

## Example

```python
from gooddata_api_client.models.declarative_export_definition_request_payload import DeclarativeExportDefinitionRequestPayload

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeExportDefinitionRequestPayload from a JSON string
declarative_export_definition_request_payload_instance = DeclarativeExportDefinitionRequestPayload.from_json(json)
# print the JSON string representation of the object
print(DeclarativeExportDefinitionRequestPayload.to_json())

# convert the object into a dict
declarative_export_definition_request_payload_dict = declarative_export_definition_request_payload_instance.to_dict()
# create an instance of DeclarativeExportDefinitionRequestPayload from a dict
declarative_export_definition_request_payload_from_dict = DeclarativeExportDefinitionRequestPayload.from_dict(declarative_export_definition_request_payload_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


