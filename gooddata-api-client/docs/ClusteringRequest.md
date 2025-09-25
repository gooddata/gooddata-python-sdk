# ClusteringRequest


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number_of_clusters** | **int** | Number of clusters to create | 
**threshold** | **float** | Threshold used for algorithm | [optional] [default to 0.03]

## Example

```python
from gooddata_api_client.models.clustering_request import ClusteringRequest

# TODO update the JSON string below
json = "{}"
# create an instance of ClusteringRequest from a JSON string
clustering_request_instance = ClusteringRequest.from_json(json)
# print the JSON string representation of the object
print(ClusteringRequest.to_json())

# convert the object into a dict
clustering_request_dict = clustering_request_instance.to_dict()
# create an instance of ClusteringRequest from a dict
clustering_request_from_dict = ClusteringRequest.from_dict(clustering_request_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


