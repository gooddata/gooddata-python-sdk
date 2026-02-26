# gooddata_api_client.model.json_api_knowledge_recommendation_patch.JsonApiKnowledgeRecommendationPatch

JSON:API representation of patching knowledgeRecommendation entity.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | JSON:API representation of patching knowledgeRecommendation entity. | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[relationships](#relationships)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**[attributes](#attributes)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 
**id** | str,  | str,  | API identifier of an object | 
**type** | str,  | str,  | Object type | must be one of ["knowledgeRecommendation", ] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# attributes

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**analyticalDashboardTitle** | str,  | str,  | Human-readable title of the analytical dashboard (denormalized for display) | [optional] 
**analyzedPeriod** | str,  | str,  | Analyzed time period (e.g., &#x27;2023-07&#x27; or &#x27;July 2023&#x27;) | [optional] 
**analyzedValue** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Metric value in the analyzed period (the observed value that triggered the anomaly) | [optional] 
**areRelationsValid** | bool,  | BoolClass,  |  | [optional] 
**comparisonType** | str,  | str,  | Time period for comparison | [optional] must be one of ["MONTH", "QUARTER", "YEAR", ] 
**confidence** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Confidence score (0.0 to 1.0) | [optional] 
**description** | str,  | str,  | Description of the recommendation | [optional] 
**direction** | str,  | str,  | Direction of the metric change | [optional] must be one of ["INCREASED", "DECREASED", ] 
**metricTitle** | str,  | str,  | Human-readable title of the metric (denormalized for display) | [optional] 
**[recommendations](#recommendations)** | dict, frozendict.frozendict,  | frozendict.frozendict,  | Structured recommendations data as JSON | [optional] 
**referencePeriod** | str,  | str,  | Reference time period for comparison (e.g., &#x27;2023-06&#x27; or &#x27;Jun 2023&#x27;) | [optional] 
**referenceValue** | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO | Metric value in the reference period | [optional] 
**sourceCount** | decimal.Decimal, int,  | decimal.Decimal,  | Number of source documents used for generation | [optional] value must be a 32 bit integer
**[tags](#tags)** | list, tuple,  | tuple,  |  | [optional] 
**title** | str,  | str,  | Human-readable title for the recommendation, e.g. &#x27;Revenue decreased vs last month&#x27; | [optional] 
**widgetId** | str,  | str,  | ID of the widget where the anomaly was detected | [optional] 
**widgetName** | str,  | str,  | Name of the widget where the anomaly was detected | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# recommendations

Structured recommendations data as JSON

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | Structured recommendations data as JSON | 

# tags

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# relationships

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[analyticalDashboard](#analyticalDashboard)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | [optional] 
**[metric](#metric)** | dict, frozendict.frozendict,  | frozendict.frozendict,  |  | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# analyticalDashboard

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**data** | [**JsonApiAnalyticalDashboardToOneLinkage**](JsonApiAnalyticalDashboardToOneLinkage.md) | [**JsonApiAnalyticalDashboardToOneLinkage**](JsonApiAnalyticalDashboardToOneLinkage.md) |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# metric

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**data** | [**JsonApiMetricToOneLinkage**](JsonApiMetricToOneLinkage.md) | [**JsonApiMetricToOneLinkage**](JsonApiMetricToOneLinkage.md) |  | 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

