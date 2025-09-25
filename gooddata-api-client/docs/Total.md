# Total

Definition of a total. There are two types of totals: grand totals and subtotals. Grand total data will be returned in a separate section of the result structure while subtotals are fully integrated into the main result data. The mechanism for this distinction is automatic and it's described in `TotalDimension`

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**function** | **str** | Aggregation function to compute the total. | 
**local_identifier** | **str** | Total identification within this request. Used e.g. in sorting by a total. | 
**metric** | **str** | The metric for which the total will be computed | 
**total_dimensions** | [**List[TotalDimension]**](TotalDimension.md) |  | 

## Example

```python
from gooddata_api_client.models.total import Total

# TODO update the JSON string below
json = "{}"
# create an instance of Total from a JSON string
total_instance = Total.from_json(json)
# print the JSON string representation of the object
print(Total.to_json())

# convert the object into a dict
total_dict = total_instance.to_dict()
# create an instance of Total from a dict
total_from_dict = Total.from_dict(total_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


