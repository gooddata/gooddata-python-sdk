# gooddata_api_client.model.search_request.SearchRequest

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
dict, frozendict.frozendict,  | frozendict.frozendict,  |  | 

### Dictionary Keys
Key | Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | ------------- | -------------
**question** | str,  | str,  | Keyword/sentence is input for search. | 
**[allowedRelationshipTypes](#allowedRelationshipTypes)** | list, tuple,  | tuple,  | Filter relationships and results based on allowed relationship type combinations. When specified, only relationships matching the allowed types are returned, and results are filtered to include only direct matches or objects reachable via allowed relationships. When null or omitted, all relationships and results are returned (default behavior). Note: This filtering happens after the initial search, so the number of returned results may be lower than the requested limit if some results are filtered out. | [optional] 
**deepSearch** | bool,  | BoolClass,  | Turn on deep search. If true, content of complex objects will be searched as well, e.g. metrics in visualizations. | [optional] if omitted the server will use the default value of False
**enableHybridSearch** | bool,  | BoolClass,  | If true, enables hybrid search combining vector similarity and keyword matching. This can improve search results by considering both semantic similarity and exact keyword matches. | [optional] if omitted the server will use the default value of False
**[excludeTags](#excludeTags)** | list, tuple,  | tuple,  | Exclude objects that contain any of the specified tags. This parameter only affects the search results. Objects with excluded tags are completely hidden from the results. | [optional] 
**includeHidden** | bool,  | BoolClass,  | If true, includes hidden objects in search results. If false (default), excludes objects where isHidden&#x3D;true. | [optional] if omitted the server will use the default value of False
**[includeTags](#includeTags)** | list, tuple,  | tuple,  | Include only objects that contain at least one of the specified tags (OR logic). This parameter only affects the search results. If an object has multiple tags, it will be included as long as it matches at least one tag from this parameter. | [optional] 
**limit** | decimal.Decimal, int,  | decimal.Decimal,  | Maximum number of results to return. There is a hard limit and the actual number of returned results may be lower than what is requested. This can happen when post-search filters are applied (e.g., reranker threshold filtering or allowedRelationshipTypes filtering), which may exclude some results after the initial search. | [optional] if omitted the server will use the default value of 10value must be a 32 bit integer
**[objectTypes](#objectTypes)** | list, tuple,  | tuple,  | List of object types to search for. | [optional] 
**relevantScoreThreshold** | decimal.Decimal, int, float,  | decimal.Decimal,  | Score, above which we return found objects. Below this score objects are not relevant. | [optional] if omitted the server will use the default value of 0.3value must be a 64 bit float
**titleToDescriptorRatio** | decimal.Decimal, int, float,  | decimal.Decimal,  | Temporary for experiments. Ratio of title score to descriptor score. | [optional] if omitted the server will use the default value of 0.7value must be a 64 bit float
**any_string_name** | dict, frozendict.frozendict, str, date, datetime, int, float, bool, decimal.Decimal, None, list, tuple, bytes, io.FileIO, io.BufferedReader | frozendict.frozendict, str, BoolClass, decimal.Decimal, NoneClass, tuple, bytes, FileIO | any string name can be used but the value must be the correct type | [optional]

# allowedRelationshipTypes

Filter relationships and results based on allowed relationship type combinations. When specified, only relationships matching the allowed types are returned, and results are filtered to include only direct matches or objects reachable via allowed relationships. When null or omitted, all relationships and results are returned (default behavior). Note: This filtering happens after the initial search, so the number of returned results may be lower than the requested limit if some results are filtered out.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Filter relationships and results based on allowed relationship type combinations. When specified, only relationships matching the allowed types are returned, and results are filtered to include only direct matches or objects reachable via allowed relationships. When null or omitted, all relationships and results are returned (default behavior). Note: This filtering happens after the initial search, so the number of returned results may be lower than the requested limit if some results are filtered out. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
[**AllowedRelationshipType**](AllowedRelationshipType.md) | [**AllowedRelationshipType**](AllowedRelationshipType.md) | [**AllowedRelationshipType**](AllowedRelationshipType.md) |  | 

# excludeTags

Exclude objects that contain any of the specified tags. This parameter only affects the search results. Objects with excluded tags are completely hidden from the results.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Exclude objects that contain any of the specified tags. This parameter only affects the search results. Objects with excluded tags are completely hidden from the results. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Tag to exclude. | 

# includeTags

Include only objects that contain at least one of the specified tags (OR logic). This parameter only affects the search results. If an object has multiple tags, it will be included as long as it matches at least one tag from this parameter.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Include only objects that contain at least one of the specified tags (OR logic). This parameter only affects the search results. If an object has multiple tags, it will be included as long as it matches at least one tag from this parameter. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Tag to include. | 

# objectTypes

List of object types to search for.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | List of object types to search for. | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  | Object type to search for. | must be one of ["attribute", "metric", "fact", "label", "date", "dataset", "visualization", "dashboard", ] 

[[Back to Model list]](../../README.md#documentation-for-models) [[Back to API list]](../../README.md#documentation-for-api-endpoints) [[Back to README]](../../README.md)

