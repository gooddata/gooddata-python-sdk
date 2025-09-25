# JsonApiDashboardPluginPatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiDashboardPluginPatch**](JsonApiDashboardPluginPatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_dashboard_plugin_patch_document import JsonApiDashboardPluginPatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDashboardPluginPatchDocument from a JSON string
json_api_dashboard_plugin_patch_document_instance = JsonApiDashboardPluginPatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiDashboardPluginPatchDocument.to_json())

# convert the object into a dict
json_api_dashboard_plugin_patch_document_dict = json_api_dashboard_plugin_patch_document_instance.to_dict()
# create an instance of JsonApiDashboardPluginPatchDocument from a dict
json_api_dashboard_plugin_patch_document_from_dict = JsonApiDashboardPluginPatchDocument.from_dict(json_api_dashboard_plugin_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


