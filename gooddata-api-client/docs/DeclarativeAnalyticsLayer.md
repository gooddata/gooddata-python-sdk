# DeclarativeAnalyticsLayer


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**analytical_dashboard_extensions** | [**List[DeclarativeAnalyticalDashboardExtension]**](DeclarativeAnalyticalDashboardExtension.md) | A list of dashboard permissions assigned to a related dashboard. | [optional] 
**analytical_dashboards** | [**List[DeclarativeAnalyticalDashboard]**](DeclarativeAnalyticalDashboard.md) | A list of analytical dashboards available in the model. | [optional] 
**attribute_hierarchies** | [**List[DeclarativeAttributeHierarchy]**](DeclarativeAttributeHierarchy.md) | A list of attribute hierarchies. | [optional] 
**dashboard_plugins** | [**List[DeclarativeDashboardPlugin]**](DeclarativeDashboardPlugin.md) | A list of dashboard plugins available in the model. | [optional] 
**export_definitions** | [**List[DeclarativeExportDefinition]**](DeclarativeExportDefinition.md) | A list of export definitions. | [optional] 
**filter_contexts** | [**List[DeclarativeFilterContext]**](DeclarativeFilterContext.md) | A list of filter contexts available in the model. | [optional] 
**metrics** | [**List[DeclarativeMetric]**](DeclarativeMetric.md) | A list of metrics available in the model. | [optional] 
**visualization_objects** | [**List[DeclarativeVisualizationObject]**](DeclarativeVisualizationObject.md) | A list of visualization objects available in the model. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_analytics_layer import DeclarativeAnalyticsLayer

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeAnalyticsLayer from a JSON string
declarative_analytics_layer_instance = DeclarativeAnalyticsLayer.from_json(json)
# print the JSON string representation of the object
print(DeclarativeAnalyticsLayer.to_json())

# convert the object into a dict
declarative_analytics_layer_dict = declarative_analytics_layer_instance.to_dict()
# create an instance of DeclarativeAnalyticsLayer from a dict
declarative_analytics_layer_from_dict = DeclarativeAnalyticsLayer.from_dict(declarative_analytics_layer_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


