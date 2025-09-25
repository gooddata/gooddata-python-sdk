# JsonApiAnalyticalDashboardOutDocument


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**JsonApiAnalyticalDashboardOut**](JsonApiAnalyticalDashboardOut.md) |  | 
**included** | [**List[JsonApiAnalyticalDashboardOutIncludes]**](JsonApiAnalyticalDashboardOutIncludes.md) | Included resources | [optional] 
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_analytical_dashboard_out_document import JsonApiAnalyticalDashboardOutDocument

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiAnalyticalDashboardOutDocument from a JSON string
json_api_analytical_dashboard_out_document_instance = JsonApiAnalyticalDashboardOutDocument.from_json(json)
# print the JSON string representation of the object
print(JsonApiAnalyticalDashboardOutDocument.to_json())

# convert the object into a dict
json_api_analytical_dashboard_out_document_dict = json_api_analytical_dashboard_out_document_instance.to_dict()
# create an instance of JsonApiAnalyticalDashboardOutDocument from a dict
json_api_analytical_dashboard_out_document_from_dict = JsonApiAnalyticalDashboardOutDocument.from_dict(json_api_analytical_dashboard_out_document_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


