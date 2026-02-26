# gooddata_api_client.model.aac_analytics_model.AacAnalyticsModel

AAC analytics model representation compatible with Analytics-as-Code YAML format.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | AAC analytics model representation compatible with Analytics-as-Code YAML format. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[attribute_hierarchies](#attribute_hierarchies)** | list, tuple,  | tuple,  | An array of attribute hierarchies. | [optional] 
**[dashboards](#dashboards)** | list, tuple,  | tuple,  | An array of dashboards. | [optional] 
**[metrics](#metrics)** | list, tuple,  | tuple,  | An array of metrics. | [optional] 
**[plugins](#plugins)** | list, tuple,  | tuple,  | An array of dashboard plugins. | [optional] 
**[visualizations](#visualizations)** | list, tuple,  | tuple,  | An array of visualizations. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attribute_hierarchies

An array of attribute hierarchies.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of attribute hierarchies. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacAttributeHierarchy**](AacAttributeHierarchy.md) | [**AacAttributeHierarchy**](AacAttributeHierarchy.md) | [**AacAttributeHierarchy**](AacAttributeHierarchy.md) |  | 

# dashboards

An array of dashboards.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of dashboards. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacDashboard**](AacDashboard.md) | [**AacDashboard**](AacDashboard.md) | [**AacDashboard**](AacDashboard.md) |  | 

# metrics

An array of metrics.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of metrics. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacMetric**](AacMetric.md) | [**AacMetric**](AacMetric.md) | [**AacMetric**](AacMetric.md) |  | 

# plugins

An array of dashboard plugins.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of dashboard plugins. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacPlugin**](AacPlugin.md) | [**AacPlugin**](AacPlugin.md) | [**AacPlugin**](AacPlugin.md) |  | 

# visualizations

An array of visualizations.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | An array of visualizations. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AacVisualization**](AacVisualization.md) | [**AacVisualization**](AacVisualization.md) | [**AacVisualization**](AacVisualization.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

