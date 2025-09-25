# CreatedVisualizationFiltersInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**exclude** | **List[str]** |  | 
**using** | **str** |  | 
**include** | **List[str]** |  | 
**var_from** | **int** |  | 
**to** | **int** |  | 
**granularity** | **str** |  | 
**ranking_filter** | [**RankingFilterRankingFilter**](RankingFilterRankingFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.created_visualization_filters_inner import CreatedVisualizationFiltersInner

# TODO update the JSON string below
json = "{}"
# create an instance of CreatedVisualizationFiltersInner from a JSON string
created_visualization_filters_inner_instance = CreatedVisualizationFiltersInner.from_json(json)
# print the JSON string representation of the object
print(CreatedVisualizationFiltersInner.to_json())

# convert the object into a dict
created_visualization_filters_inner_dict = created_visualization_filters_inner_instance.to_dict()
# create an instance of CreatedVisualizationFiltersInner from a dict
created_visualization_filters_inner_from_dict = CreatedVisualizationFiltersInner.from_dict(created_visualization_filters_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


