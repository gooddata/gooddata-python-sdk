# TotalDimension

A list of dimensions across which the total will be computed. Total headers for only these dimensions will be returned in the result.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**dimension_identifier** | **str** | An identifier of a dimension for which the total will be computed. | 
**total_dimension_items** | **List[str]** | List of dimension items which will be used for total computation. The total is a grand total in this dimension if the list is empty or it includes the first dimension item from the dimension definition, and its data and header will be returned in a separate &#x60;ExecutionResultGrandTotal&#x60; structure. Otherwise, it is a subtotal and the data will be integrated into the main result. | 

## Example

```python
from gooddata_api_client.models.total_dimension import TotalDimension

# TODO update the JSON string below
json = "{}"
# create an instance of TotalDimension from a JSON string
total_dimension_instance = TotalDimension.from_json(json)
# print the JSON string representation of the object
print(TotalDimension.to_json())

# convert the object into a dict
total_dimension_dict = total_dimension_instance.to_dict()
# create an instance of TotalDimension from a dict
total_dimension_from_dict = TotalDimension.from_dict(total_dimension_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


