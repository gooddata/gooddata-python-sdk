# JsonApiVisualizationObjectOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiVisualizationObjectOut**](JsonApiVisualizationObjectOut.md) |  | 
**included** | [**List[JsonApiMetricOutIncludes]**](JsonApiMetricOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_visualization_object_out_document import JsonApiVisualizationObjectOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiVisualizationObjectOutDocument from a JSON string
json_api_visualization_object_out_document_instance = JsonApiVisualizationObjectOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiVisualizationObjectOutDocument.to_json())

# convert the object into a dict
json_api_visualization_object_out_document_dict = json_api_visualization_object_out_document_instance.to_dict()
# create an instance of JsonApiVisualizationObjectOutDocument from a dict
json_api_visualization_object_out_document_from_dict = JsonApiVisualizationObjectOutDocument.from_dict(json_api_visualization_object_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


