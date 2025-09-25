# ListLinks


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**var_self** | **str** | A string containing the link&#39;s URL. | 
**next** | **str** | A string containing the link&#39;s URL for the next page of data. | [optional] 

## Example

```python
from gooddata_api_client.models.list_links import ListLinks

# TODO update the JSON string below
json = "{}"
# create an instance of ListLinks from a JSON string
list_links_instance = ListLinks.from_json(json)
# print the JSON string representation of the object
print(ListLinks.to_json())

# convert the object into a dict
list_links_dict = list_links_instance.to_dict()
# create an instance of ListLinks from a dict
list_links_from_dict = ListLinks.from_dict(list_links_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


