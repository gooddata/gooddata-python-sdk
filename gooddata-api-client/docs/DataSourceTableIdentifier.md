# DataSourceTableIdentifier

An id of the table. Including ID of data source.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_source_id** | **str** | Data source ID. | 
**id** | **str** | ID of table. | 
**path** | **List[str]** | Path to table. | [optional] 
**type** | **str** | Data source entity type. | 

## Example

```python
from gooddata_api_client.models.data_source_table_identifier import DataSourceTableIdentifier

# TODO update the JSON string below
json = "{}"
# create an instance of DataSourceTableIdentifier from a JSON string
data_source_table_identifier_instance = DataSourceTableIdentifier.from_json(json)
# print the JSON string representation of the object
print(DataSourceTableIdentifier.to_json())

# convert the object into a dict
data_source_table_identifier_dict = data_source_table_identifier_instance.to_dict()
# create an instance of DataSourceTableIdentifier from a dict
data_source_table_identifier_from_dict = DataSourceTableIdentifier.from_dict(data_source_table_identifier_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


