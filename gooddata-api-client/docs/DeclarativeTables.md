# DeclarativeTables

A physical data model (PDM) tables.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**tables** | [**List[DeclarativeTable]**](DeclarativeTable.md) | An array of physical database tables. | 

## Example

```python
from gooddata_api_client.models.declarative_tables import DeclarativeTables

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeTables from a JSON string
declarative_tables_instance = DeclarativeTables.from_json(json)
# print the JSON string representation of the object
print(DeclarativeTables.to_json())

# convert the object into a dict
declarative_tables_dict = declarative_tables_instance.to_dict()
# create an instance of DeclarativeTables from a dict
declarative_tables_from_dict = DeclarativeTables.from_dict(declarative_tables_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


