# SearchRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**question** | **str** | Keyword/sentence is input for search. | 
**deep_search** | **bool** | Turn on deep search. If true, content of complex objects will be searched as well, e.g. metrics in visualizations. | [optional]  if omitted the server will use the default value of False
**limit** | **int** | Maximum number of results to return. There is a hard limit and the actual number of returned results may be lower than what is requested. | [optional]  if omitted the server will use the default value of 10
**object_types** | **[str]** | List of object types to search for. | [optional] 
**relevant_score_threshold** | **float** | Score, above which we return found objects. Below this score objects are not relevant. | [optional]  if omitted the server will use the default value of 0.3
**title_to_descriptor_ratio** | **float** | Temporary for experiments. Ratio of title score to descriptor score. | [optional]  if omitted the server will use the default value of 0.7
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


