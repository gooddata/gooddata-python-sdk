# PageMetadata


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**number** | **int** | The number of the current page | [optional] 
**size** | **int** | The size of the current page | [optional] 
**total_elements** | **int** | The total number of elements | [optional] 
**total_pages** | **int** | The total number of pages | [optional] 

## Example

```python
from gooddata_api_client.models.page_metadata import PageMetadata

# TODO update the JSON string below
json = "{}"
# create an instance of PageMetadata from a JSON string
page_metadata_instance = PageMetadata.from_json(json)
# print the JSON string representation of the object
print(PageMetadata.to_json())

# convert the object into a dict
page_metadata_dict = page_metadata_instance.to_dict()
# create an instance of PageMetadata from a dict
page_metadata_from_dict = PageMetadata.from_dict(page_metadata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


