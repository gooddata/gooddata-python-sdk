# ElementsRequestDependsOnInner


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**complement_filter** | **bool** | Inverse filtering mode. | [optional] [default to False]
**label** | **str** | Specifies on which label the filter depends on. | 
**values** | **List[Optional[str]]** | Specifies values of the label for element filtering. | 
**date_filter** | [**DateFilter**](DateFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.elements_request_depends_on_inner import ElementsRequestDependsOnInner

# TODO update the JSON string below
json = "{}"
# create an instance of ElementsRequestDependsOnInner from a JSON string
elements_request_depends_on_inner_instance = ElementsRequestDependsOnInner.from_json(json)
# print the JSON string representation of the object
print(ElementsRequestDependsOnInner.to_json())

# convert the object into a dict
elements_request_depends_on_inner_dict = elements_request_depends_on_inner_instance.to_dict()
# create an instance of ElementsRequestDependsOnInner from a dict
elements_request_depends_on_inner_from_dict = ElementsRequestDependsOnInner.from_dict(elements_request_depends_on_inner_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


