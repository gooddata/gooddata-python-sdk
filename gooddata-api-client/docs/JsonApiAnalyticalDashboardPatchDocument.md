# JsonApiAnalyticalDashboardPatchDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiAnalyticalDashboardPatch**](JsonApiAnalyticalDashboardPatch.md) |  | 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_patch_document import JsonApiAnalyticalDashboardPatchDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardPatchDocument from a JSON string
json_api_analytical_dashboard_patch_document_instance = JsonApiAnalyticalDashboardPatchDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardPatchDocument.to_json())

# convert the object into a dict
json_api_analytical_dashboard_patch_document_dict = json_api_analytical_dashboard_patch_document_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardPatchDocument from a dict
json_api_analytical_dashboard_patch_document_from_dict = JsonApiAnalyticalDashboardPatchDocument.from_dict(json_api_analytical_dashboard_patch_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


