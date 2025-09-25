# VisibleFilter


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**is_all_time_date_filter** | **bool** | Indicates if the filter is an all-time date filter. Such a filter is not included in report computation, so there is no filter with the same &#39;localIdentifier&#39; to be found. In such cases, this flag is used to inform the server to not search for the filter in the definitions and include it anyways. | [optional] [default to False]
**local_identifier** | **str** |  | [optional] 
**title** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.visible_filter import VisibleFilter

# TODO update the JSON string below
json = "{}"
# create an instance of VisibleFilter from a JSON string
visible_filter_instance = VisibleFilter.from_json(json)
# print the JSON string representation of the object
print(VisibleFilter.to_json())

# convert the object into a dict
visible_filter_dict = visible_filter_instance.to_dict()
# create an instance of VisibleFilter from a dict
visible_filter_from_dict = VisibleFilter.from_dict(visible_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


