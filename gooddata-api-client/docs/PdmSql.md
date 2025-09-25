# PdmSql

SQL dataset definition.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**columns** | [**List[SqlColumn]**](SqlColumn.md) | Columns defining SQL dataset. | [optional] 
**statement** | **str** | SQL statement. | 
**title** | **str** | SQL dataset title. | 

## Example

```python
from gooddata_api_client.models.pdm_sql import PdmSql

# TODO update the JSON string below
json = "{}"
# create an instance of PdmSql from a JSON string
pdm_sql_instance = PdmSql.from_json(json)
# print the JSON string representation of the object
print(PdmSql.to_json())

# convert the object into a dict
pdm_sql_dict = pdm_sql_instance.to_dict()
# create an instance of PdmSql from a dict
pdm_sql_from_dict = PdmSql.from_dict(pdm_sql_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


