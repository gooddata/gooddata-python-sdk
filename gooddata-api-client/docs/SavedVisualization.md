# SavedVisualization

Created and saved visualization IDs.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**created_visualization_id** | **str** | Created visualization ID. | 
**saved_visualization_id** | **str** | Saved visualization ID. | 

## Example

```python
from gooddata_api_client.models.saved_visualization import SavedVisualization

# TODO update the JSON string below
json = "{}"
# create an instance of SavedVisualization from a JSON string
saved_visualization_instance = SavedVisualization.from_json(json)
# print the JSON string representation of the object
print(SavedVisualization.to_json())

# convert the object into a dict
saved_visualization_dict = saved_visualization_instance.to_dict()
# create an instance of SavedVisualization from a dict
saved_visualization_from_dict = SavedVisualization.from_dict(saved_visualization_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


