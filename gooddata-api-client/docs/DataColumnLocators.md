# DataColumnLocators

Data column locators for the values.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | [**Dict[str, DataColumnLocator]**](DataColumnLocator.md) | Mapping from dimensions to data column locators. | [optional] 

## Example

```python
from gooddata_api_client.models.data_column_locators import DataColumnLocators

# TODO update the JSON string below
json = "{}"
# create an instance of DataColumnLocators from a JSON string
data_column_locators_instance = DataColumnLocators.from_json(json)
# print the JSON string representation of the object
print(DataColumnLocators.to_json())

# convert the object into a dict
data_column_locators_dict = data_column_locators_instance.to_dict()
# create an instance of DataColumnLocators from a dict
data_column_locators_from_dict = DataColumnLocators.from_dict(data_column_locators_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


