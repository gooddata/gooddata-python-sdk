# JsonApiExportTemplateOut

JSON:API representation of exportTemplate entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiExportTemplateInAttributes**](JsonApiExportTemplateInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_export_template_out import JsonApiExportTemplateOut

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportTemplateOut from a JSON string
json_api_export_template_out_instance = JsonApiExportTemplateOut.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportTemplateOut.to_json())

# convert the object into a dict
json_api_export_template_out_dict = json_api_export_template_out_instance.to_dict()
# create an instance of JsonApiExportTemplateOut from a dict
json_api_export_template_out_from_dict = JsonApiExportTemplateOut.from_dict(json_api_export_template_out_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


