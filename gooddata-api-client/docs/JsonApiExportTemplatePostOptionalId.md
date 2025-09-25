# JsonApiExportTemplatePostOptionalId

JSON:API representation of exportTemplate entity.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attributes** | [**JsonApiExportTemplateInAttributes**](JsonApiExportTemplateInAttributes.md) |  | 
**id** | **str** | API identifier of an object | [optional] 
**type** | **str** | Object type | 

## Example

```python
from gooddata_api_client.models.json_api_export_template_post_optional_id import JsonApiExportTemplatePostOptionalId

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiExportTemplatePostOptionalId from a JSON string
json_api_export_template_post_optional_id_instance = JsonApiExportTemplatePostOptionalId.from_json(json)
# print the JSON string representation of the object
print(JsonApiExportTemplatePostOptionalId.to_json())

# convert the object into a dict
json_api_export_template_post_optional_id_dict = json_api_export_template_post_optional_id_instance.to_dict()
# create an instance of JsonApiExportTemplatePostOptionalId from a dict
json_api_export_template_post_optional_id_from_dict = JsonApiExportTemplatePostOptionalId.from_dict(json_api_export_template_post_optional_id_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


