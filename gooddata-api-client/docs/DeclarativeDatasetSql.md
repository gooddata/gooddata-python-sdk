# DeclarativeDatasetSql

SQL defining this dataset.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_source_id** | **str** | Data source ID. | 
**statement** | **str** | SQL statement. | 

## Example

```python
from gooddata_api_client.models.declarative_dataset_sql import DeclarativeDatasetSql

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDatasetSql from a JSON string
declarative_dataset_sql_instance = DeclarativeDatasetSql.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDatasetSql.to_json())

# convert the object into a dict
declarative_dataset_sql_dict = declarative_dataset_sql_instance.to_dict()
# create an instance of DeclarativeDatasetSql from a dict
declarative_dataset_sql_from_dict = DeclarativeDatasetSql.from_dict(declarative_dataset_sql_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


