# ElementsResponse

Entity holding list of sorted & filtered label elements, related primary label of attribute owning requested label and paging.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cache_id** | **str** | The client can use this in subsequent requests (like paging or search) to get results from the same point in time as the previous request. This is useful when the underlying data source has caches disabled and the client wants to avoid seeing inconsistent results and to also avoid excessive queries to the database itself. | [optional] 
**elements** | [**List[Element]**](Element.md) | List of returned elements. | 
**format** | [**AttributeFormat**](AttributeFormat.md) |  | [optional] 
**granularity** | **str** | Granularity of requested label in case of date attribute | [optional] 
**paging** | [**Paging**](Paging.md) |  | 
**primary_label** | [**RestApiIdentifier**](RestApiIdentifier.md) |  | 

## Example

```python
from gooddata_api_client.models.elements_response import ElementsResponse

# TODO update the JSON string below
json = "{}"
# create an instance of ElementsResponse from a JSON string
elements_response_instance = ElementsResponse.from_json(json)
# print the JSON string representation of the object
print(ElementsResponse.to_json())

# convert the object into a dict
elements_response_dict = elements_response_instance.to_dict()
# create an instance of ElementsResponse from a dict
elements_response_from_dict = ElementsResponse.from_dict(elements_response_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


