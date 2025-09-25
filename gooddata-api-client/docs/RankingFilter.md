# RankingFilter

Filter the result on top/bottom N values according to given metric(s).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**ranking_filter** | [**RankingFilterRankingFilter**](RankingFilterRankingFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.ranking_filter import RankingFilter

# TODO update the JSON string below
json = "{}"
# create an instance of RankingFilter from a JSON string
ranking_filter_instance = RankingFilter.from_json(json)
# print the JSON string representation of the object
print(RankingFilter.to_json())

# convert the object into a dict
ranking_filter_dict = ranking_filter_instance.to_dict()
# create an instance of RankingFilter from a dict
ranking_filter_from_dict = RankingFilter.from_dict(ranking_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


