# SearchRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**deep_search** | **bool** | Turn on deep search. If true, content of complex objects will be searched as well, e.g. metrics in visualizations. | [optional] [default to False]
**include_hidden** | **bool** | If true, includes hidden objects in search results. If false (default), excludes objects where isHidden&#x3D;true. | [optional] [default to False]
**limit** | **int** | Maximum number of results to return. There is a hard limit and the actual number of returned results may be lower than what is requested. | [optional] [default to 10]
**object_types** | **List[str]** | List of object types to search for. | [optional] 
**question** | **str** | Keyword/sentence is input for search. | 
**relevant_score_threshold** | **float** | Score, above which we return found objects. Below this score objects are not relevant. | [optional] [default to 0.3]
**title_to_descriptor_ratio** | **float** | Temporary for experiments. Ratio of title score to descriptor score. | [optional] [default to 0.7]

## Example

```python
from gooddata_api_client.models.search_request import SearchRequest

# TODO update the JSON string below
json = "{}"
# create an instance of SearchRequest from a JSON string
search_request_instance = SearchRequest.from_json(json)
# print the JSON string representation of the object
print(SearchRequest.to_json())

# convert the object into a dict
search_request_dict = search_request_instance.to_dict()
# create an instance of SearchRequest from a dict
search_request_from_dict = SearchRequest.from_dict(search_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


