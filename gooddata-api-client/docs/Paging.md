# Paging

Current page description.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**count** | **int** | Count of items in this page. | 
**next** | **str** | Link to next page, or null if this is last page. | [optional] 
**offset** | **int** | Offset of this page. | 
**total** | **int** | Count of returnable items ignoring paging. | 

## Example

```python
from gooddata_api_client.models.paging import Paging

# TODO update the JSON string below
json = "{}"
# create an instance of Paging from a JSON string
paging_instance = Paging.from_json(json)
# print the JSON string representation of the object
print(Paging.to_json())

# convert the object into a dict
paging_dict = paging_instance.to_dict()
# create an instance of Paging from a dict
paging_from_dict = Paging.from_dict(paging_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


