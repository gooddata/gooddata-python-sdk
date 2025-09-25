# DeclarativeColumn

A table column.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_type** | **str** | Column type | 
**is_primary_key** | **bool** | Is column part of primary key? | [optional] 
**name** | **str** | Column name | 
**referenced_table_column** | **str** | Referenced table (Foreign key) | [optional] 
**referenced_table_id** | **str** | Referenced table (Foreign key) | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_column import DeclarativeColumn

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeColumn from a JSON string
declarative_column_instance = DeclarativeColumn.from_json(json)
# print the JSON string representation of the object
print(DeclarativeColumn.to_json())

# convert the object into a dict
declarative_column_dict = declarative_column_instance.to_dict()
# create an instance of DeclarativeColumn from a dict
declarative_column_from_dict = DeclarativeColumn.from_dict(declarative_column_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


