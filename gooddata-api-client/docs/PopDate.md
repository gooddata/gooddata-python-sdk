# PopDate

Combination of the date attribute to use and how many periods ago to calculate the PoP for.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**attribute** | [**AfmObjectIdentifierAttribute**](AfmObjectIdentifierAttribute.md) |  | 
**periods_ago** | **int** | Number of periods ago to calculate the previous period for. | 

## Example

```python
from gooddata_api_client.models.pop_date import PopDate

# TODO update the JSON string below
json = "{}"
# create an instance of PopDate from a JSON string
pop_date_instance = PopDate.from_json(json)
# print the JSON string representation of the object
print(PopDate.to_json())

# convert the object into a dict
pop_date_dict = pop_date_instance.to_dict()
# create an instance of PopDate from a dict
pop_date_from_dict = PopDate.from_dict(pop_date_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


