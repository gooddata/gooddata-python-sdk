# JsonApiExportTemplateIn

JSON:API representation of exportTemplate entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiExportTemplateInAttributes**](JsonApiExportTemplateInAttributes.md) |  | 
**id** | **str** | API identifier of an object | 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_export_template_in import JsonApiExportTemplateIn

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportTemplateIn from a JSON string
json_api_export_template_in_instance = JsonApiExportTemplateIn.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportTemplateIn.to_json())

# convert the object into a dict
json_api_export_template_in_dict = json_api_export_template_in_instance.to_dict()
# create an instance of JsonApiExportTemplateIn from a dict
json_api_export_template_in_from_dict = JsonApiExportTemplateIn.from_dict(json_api_export_template_in_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


