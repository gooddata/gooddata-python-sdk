# RankingFilterRankingFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**apply_on_result** | **bool** |  | [optional] 
**dimensionality** | [**List[AfmIdentifier]**](AfmIdentifier.md) | References to the attributes to be used when filtering. | [optional] 
**local_identifier** | **str** |  | [optional] 
**measures** | [**List[AfmIdentifier]**](AfmIdentifier.md) | References to the metrics to be used when filtering. | 
**operator** | **str** | The type of ranking to use, TOP or BOTTOM. | 
**value** | **int** | Number of top/bottom values to filter. | 

## Example

```python
from gooddata_api_client.models.ranking_filter_ranking_filter import RankingFilterRankingFilter

# TODO update the JSON string below
json = "{}"
# create an instance of RankingFilterRankingFilter from a JSON string
ranking_filter_ranking_filter_instance = RankingFilterRankingFilter.from_json(json)
# print the JSON string representation of the object
print(RankingFilterRankingFilter.to_json())

# convert the object into a dict
ranking_filter_ranking_filter_dict = ranking_filter_ranking_filter_instance.to_dict()
# create an instance of RankingFilterRankingFilter from a dict
ranking_filter_ranking_filter_from_dict = RankingFilterRankingFilter.from_dict(ranking_filter_ranking_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


