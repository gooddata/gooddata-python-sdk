# DataSourceSchemata

Result of getSchemata. Contains list of available DB schema names.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**schema_names** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.data_source_schemata import DataSourceSchemata

# TODO update the JSON string below
json = "{}"
# create an instance of DataSourceSchemata from a JSON string
data_source_schemata_instance = DataSourceSchemata.from_json(json)
# print the JSON string representation of the object
print(DataSourceSchemata.to_json())

# convert the object into a dict
data_source_schemata_dict = data_source_schemata_instance.to_dict()
# create an instance of DataSourceSchemata from a dict
data_source_schemata_from_dict = DataSourceSchemata.from_dict(data_source_schemata_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


