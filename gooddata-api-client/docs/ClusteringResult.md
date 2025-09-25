# ClusteringResult


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | **List[object]** |  | 
**clusters** | **List[Optional[int]]** |  | 
**x_coord** | **List[Optional[float]]** |  | [optional] 
**xcoord** | **List[float]** |  | 
**y_coord** | **List[Optional[float]]** |  | [optional] 
**ycoord** | **List[float]** |  | 

## Example

```python
from gooddata_api_client.models.clustering_result import ClusteringResult

# TODO update the JSON string below
json = "{}"
# create an instance of ClusteringResult from a JSON string
clustering_result_instance = ClusteringResult.from_json(json)
# print the JSON string representation of the object
print(ClusteringResult.to_json())

# convert the object into a dict
clustering_result_dict = clustering_result_instance.to_dict()
# create an instance of ClusteringResult from a dict
clustering_result_from_dict = ClusteringResult.from_dict(clustering_result_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


