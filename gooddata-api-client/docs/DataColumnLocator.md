# DataColumnLocator

Mapping from dimension items (either 'localIdentifier' from 'AttributeItem', or \"measureGroup\") to their respective values. This effectively specifies the path (location) of the data column used for sorting. Therefore values for all dimension items must be specified.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**properties** | **Dict[str, str]** | Mapping from dimension items (either &#39;localIdentifier&#39; from &#39;AttributeItem&#39;, or \&quot;measureGroup\&quot;) to their respective values. This effectively specifies the path (location) of the data column used for sorting. Therefore values for all dimension items must be specified. | 

## Example

```python
from gooddata_api_client.models.data_column_locator import DataColumnLocator

# TODO update the JSON string below
json = "{}"
# create an instance of DataColumnLocator from a JSON string
data_column_locator_instance = DataColumnLocator.from_json(json)
# print the JSON string representation of the object
print(DataColumnLocator.to_json())

# convert the object into a dict
data_column_locator_dict = data_column_locator_instance.to_dict()
# create an instance of DataColumnLocator from a dict
data_column_locator_from_dict = DataColumnLocator.from_dict(data_column_locator_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


