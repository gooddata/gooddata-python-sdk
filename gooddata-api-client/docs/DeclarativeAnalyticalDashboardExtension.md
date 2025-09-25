# DeclarativeAnalyticalDashboardExtension


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Analytical dashboard ID. | 
**permissions** | [**List[DeclarativeAnalyticalDashboardPermissionsInner]**](DeclarativeAnalyticalDashboardPermissionsInner.md) | A list of permissions. | 

## Example

```python
from gooddata_api_client.models.declarative_analytical_dashboard_extension import DeclarativeAnalyticalDashboardExtension

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalyticalDashboardExtension from a JSON string
declarative_analytical_dashboard_extension_instance = DeclarativeAnalyticalDashboardExtension.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalyticalDashboardExtension.to_json())

# convert the object into a dict
declarative_analytical_dashboard_extension_dict = declarative_analytical_dashboard_extension_instance.to_dict()
# create an instance of DeclarativeAnalyticalDashboardExtension from a dict
declarative_analytical_dashboard_extension_from_dict = DeclarativeAnalyticalDashboardExtension.from_dict(declarative_analytical_dashboard_extension_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


