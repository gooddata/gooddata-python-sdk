# DeclarativeTable

A database table.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[DeclarativeColumn]**](DeclarativeColumn.md) | An array of physical columns | 
**id** | **str** | Table id. | 
**name_prefix** | **str** | Table or view name prefix used in scan. Will be stripped when generating LDM. | [optional] 
**path** | **List[str]** | Path to table. | 
**type** | **str** | Table type: TABLE or VIEW. | 

## Example

```python
from gooddata_api_client.models.declarative_table import DeclarativeTable

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeTable from a JSON string
declarative_table_instance = DeclarativeTable.from_json(json)
# print the JSON string representation of the object
print(DeclarativeTable.to_json())

# convert the object into a dict
declarative_table_dict = declarative_table_instance.to_dict()
# create an instance of DeclarativeTable from a dict
declarative_table_from_dict = DeclarativeTable.from_dict(declarative_table_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


