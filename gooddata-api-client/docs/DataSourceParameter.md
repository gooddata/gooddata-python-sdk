# DataSourceParameter

A parameter for testing data source connection

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | Parameter name. | 
**value** | **str** | Parameter value. | 

## Example

```python
from gooddata_api_client.models.data_source_parameter import DataSourceParameter

# TODO update the JSON string below
json = "{}"
# create an instance of DataSourceParameter from a JSON string
data_source_parameter_instance = DataSourceParameter.from_json(json)
# print the JSON string representation of the object
print(DataSourceParameter.to_json())

# convert the object into a dict
data_source_parameter_dict = data_source_parameter_instance.to_dict()
# create an instance of DataSourceParameter from a dict
data_source_parameter_from_dict = DataSourceParameter.from_dict(data_source_parameter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


