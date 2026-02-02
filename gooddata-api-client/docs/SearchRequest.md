# SearchRequest


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**question** | **str** | Keyword/sentence is input for search. | 
**allowed_relationship_types** | [**[AllowedRelationshipType]**](AllowedRelationshipType.md) | Filter relationships and results based on allowed relationship type combinations. When specified, only relationships matching the allowed types are returned, and results are filtered to include only direct matches or objects reachable via allowed relationships. When null or omitted, all relationships and results are returned (default behavior). Note: This filtering happens after the initial search, so the number of returned results may be lower than the requested limit if some results are filtered out. | [optional] 
**deep_search** | **bool** | Turn on deep search. If true, content of complex objects will be searched as well, e.g. metrics in visualizations. | [optional]  if omitted the server will use the default value of False
**exclude_tags** | **[str]** | Exclude objects that contain any of the specified tags. This parameter only affects the search results. Objects with excluded tags are completely hidden from the results. | [optional] 
**include_hidden** | **bool** | If true, includes hidden objects in search results. If false (default), excludes objects where isHidden&#x3D;true. | [optional]  if omitted the server will use the default value of False
**include_tags** | **[str]** | Include only objects that contain at least one of the specified tags (OR logic). This parameter only affects the search results. If an object has multiple tags, it will be included as long as it matches at least one tag from this parameter. | [optional] 
**limit** | **int** | Maximum number of results to return. There is a hard limit and the actual number of returned results may be lower than what is requested. This can happen when post-search filters are applied (e.g., reranker threshold filtering or allowedRelationshipTypes filtering), which may exclude some results after the initial search. | [optional]  if omitted the server will use the default value of 10
**object_types** | **[str]** | List of object types to search for. | [optional] 
**relevant_score_threshold** | **float** | Score, above which we return found objects. Below this score objects are not relevant. | [optional]  if omitted the server will use the default value of 0.3
**title_to_descriptor_ratio** | **float** | Temporary for experiments. Ratio of title score to descriptor score. | [optional]  if omitted the server will use the default value of 0.7
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


