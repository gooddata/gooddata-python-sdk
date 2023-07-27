# gooddata_api_client.model.declarative_analytics_layer.DeclarativeAnalyticsLayer

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[analyticalDashboardExtensions](#analyticalDashboardExtensions)** | list, tuple,  | tuple,  | A list of dashboard permissions assigned to a related dashboard. | [optional] 
**[analyticalDashboards](#analyticalDashboards)** | list, tuple,  | tuple,  | A list of analytical dashboards available in the model. | [optional] 
**[dashboardPlugins](#dashboardPlugins)** | list, tuple,  | tuple,  | A list of dashboard plugins available in the model. | [optional] 
**[filterContexts](#filterContexts)** | list, tuple,  | tuple,  | A list of filter contexts available in the model. | [optional] 
**[metrics](#metrics)** | list, tuple,  | tuple,  | A list of metrics available in the model. | [optional] 
**[visualizationObjects](#visualizationObjects)** | list, tuple,  | tuple,  | A list of visualization objects available in the model. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# analyticalDashboardExtensions

A list of dashboard permissions assigned to a related dashboard.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of dashboard permissions assigned to a related dashboard. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeAnalyticalDashboardExtension**](DeclarativeAnalyticalDashboardExtension.md) | [**DeclarativeAnalyticalDashboardExtension**](DeclarativeAnalyticalDashboardExtension.md) | [**DeclarativeAnalyticalDashboardExtension**](DeclarativeAnalyticalDashboardExtension.md) |  | 

# analyticalDashboards

A list of analytical dashboards available in the model.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of analytical dashboards available in the model. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeAnalyticalDashboard**](DeclarativeAnalyticalDashboard.md) | [**DeclarativeAnalyticalDashboard**](DeclarativeAnalyticalDashboard.md) | [**DeclarativeAnalyticalDashboard**](DeclarativeAnalyticalDashboard.md) |  | 

# dashboardPlugins

A list of dashboard plugins available in the model.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of dashboard plugins available in the model. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeDashboardPlugin**](DeclarativeDashboardPlugin.md) | [**DeclarativeDashboardPlugin**](DeclarativeDashboardPlugin.md) | [**DeclarativeDashboardPlugin**](DeclarativeDashboardPlugin.md) |  | 

# filterContexts

A list of filter contexts available in the model.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of filter contexts available in the model. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeFilterContext**](DeclarativeFilterContext.md) | [**DeclarativeFilterContext**](DeclarativeFilterContext.md) | [**DeclarativeFilterContext**](DeclarativeFilterContext.md) |  | 

# metrics

A list of metrics available in the model.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of metrics available in the model. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeMetric**](DeclarativeMetric.md) | [**DeclarativeMetric**](DeclarativeMetric.md) | [**DeclarativeMetric**](DeclarativeMetric.md) |  | 

# visualizationObjects

A list of visualization objects available in the model.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | A list of visualization objects available in the model. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DeclarativeVisualizationObject**](DeclarativeVisualizationObject.md) | [**DeclarativeVisualizationObject**](DeclarativeVisualizationObject.md) | [**DeclarativeVisualizationObject**](DeclarativeVisualizationObject.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

