# gooddata_api_client.model.created_visualization.CreatedVisualization

List of created visualization objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  | List of created visualization objects | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**[dimensionality](#dimensionality)** | list, tuple,  | tuple,  | List of attributes representing the dimensionality of the new visualization | 
**visualizationType** | str,  | str,  | Visualization type requested in question | must be one of ["TABLE", "HEADLINE", "BAR", "LINE", "PIE", "COLUMN", "SCATTER", ] 
**[suggestions](#suggestions)** | list, tuple,  | tuple,  | Suggestions for next steps | 
**[filters](#filters)** | list, tuple,  | tuple,  | List of filters to be applied to the new visualization | 
**id** | str,  | str,  | Proposed ID of the new visualization | 
**[metrics](#metrics)** | list, tuple,  | tuple,  | List of metrics to be used in the new visualization | 
**title** | str,  | str,  | Proposed title of the new visualization | 
**config** | [**VisualizationConfig**](VisualizationConfig.md) | [**VisualizationConfig**](VisualizationConfig.md) |  | [optional] 
**savedVisualizationId** | str,  | str,  | Saved visualization ID. | [optional] 
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# dimensionality

List of attributes representing the dimensionality of the new visualization

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of attributes representing the dimensionality of the new visualization | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**DimAttribute**](DimAttribute.md) | [**DimAttribute**](DimAttribute.md) | [**DimAttribute**](DimAttribute.md) |  | 

# filters

List of filters to be applied to the new visualization

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of filters to be applied to the new visualization | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[items](#items) | dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

# items

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict, str, date, datetime, uuid.UUID, int, float, decimal.Decimal, bool, None, list, tuple, bytes, io.FileIO, io.BufferedReader,  | frozendict.frozendict, str, decimal.Decimal, BoolClass, NoneClass, tuple, bytes, FileIO |  | 

### Composed Schemas (allOf/anyOf/oneOf/not)
#### oneOf
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[AttributeNegativeFilter](AttributeNegativeFilter.md) | [**AttributeNegativeFilter**](AttributeNegativeFilter.md) | [**AttributeNegativeFilter**](AttributeNegativeFilter.md) |  | 
[AttributePositiveFilter](AttributePositiveFilter.md) | [**AttributePositiveFilter**](AttributePositiveFilter.md) | [**AttributePositiveFilter**](AttributePositiveFilter.md) |  | 
[DateAbsoluteFilter](DateAbsoluteFilter.md) | [**DateAbsoluteFilter**](DateAbsoluteFilter.md) | [**DateAbsoluteFilter**](DateAbsoluteFilter.md) |  | 
[DateRelativeFilter](DateRelativeFilter.md) | [**DateRelativeFilter**](DateRelativeFilter.md) | [**DateRelativeFilter**](DateRelativeFilter.md) |  | 
[RankingFilter](RankingFilter.md) | [**RankingFilter**](RankingFilter.md) | [**RankingFilter**](RankingFilter.md) |  | 

# metrics

List of metrics to be used in the new visualization

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of metrics to be used in the new visualization | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Metric**](Metric.md) | [**Metric**](Metric.md) | [**Metric**](Metric.md) |  | 

# suggestions

Suggestions for next steps

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Suggestions for next steps | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**Suggestion**](Suggestion.md) | [**Suggestion**](Suggestion.md) | [**Suggestion**](Suggestion.md) |  | 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

