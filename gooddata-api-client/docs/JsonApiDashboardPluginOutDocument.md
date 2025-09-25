# JsonApiDashboardPluginOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiDashboardPluginOut**](JsonApiDashboardPluginOut.md) |  | 
**included** | [**List[JsonApiUserIdentifierOutWithLinks]**](JsonApiUserIdentifierOutWithLinks.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_dashboard_plugin_out_document import JsonApiDashboardPluginOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDashboardPluginOutDocument from a JSON string
json_api_dashboard_plugin_out_document_instance = JsonApiDashboardPluginOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiDashboardPluginOutDocument.to_json())

# convert the object into a dict
json_api_dashboard_plugin_out_document_dict = json_api_dashboard_plugin_out_document_instance.to_dict()
# create an instance of JsonApiDashboardPluginOutDocument from a dict
json_api_dashboard_plugin_out_document_from_dict = JsonApiDashboardPluginOutDocument.from_dict(json_api_dashboard_plugin_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


