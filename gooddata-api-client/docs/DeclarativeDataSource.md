# DeclarativeDataSource

A data source and its properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**authentication_type** | **str** | Type of authentication used to connect to the database. | [optional] 
**cache_strategy** | **str** | Determines how the results coming from a particular datasource should be cached. - ALWAYS: The results from the datasource should be cached normally (the default). - NEVER: The results from the datasource should never be cached. | [optional] 
**client_id** | **str** | Id of client with permission to connect to the data source. | [optional] 
**client_secret** | **str** | The client secret to use to connect to the database providing the data for the data source. | [optional] 
**decoded_parameters** | [**List[Parameter]**](Parameter.md) |  | [optional] 
**id** | **str** | Data source ID. | 
**name** | **str** | Name of the data source. | 
**parameters** | [**List[Parameter]**](Parameter.md) |  | [optional] 
**password** | **str** | Password for the data-source user, property is never returned back. | [optional] 
**permissions** | [**List[DeclarativeDataSourcePermission]**](DeclarativeDataSourcePermission.md) |  | [optional] 
**private_key** | **str** | The private key to use to connect to the database providing the data for the data source. | [optional] 
**private_key_passphrase** | **str** | The passphrase used to encrypt the private key. | [optional] 
**var_schema** | **str** | A scheme/database with the data. | 
**token** | **str** | Token as an alternative to username and password. | [optional] 
**type** | **str** | Type of database. | 
**url** | **str** | An connection string relevant to type of database. | [optional] 
**username** | **str** | User with permission connect the data source/database. | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_data_source import DeclarativeDataSource

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDataSource from a JSON string
declarative_data_source_instance = DeclarativeDataSource.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDataSource.to_json())

# convert the object into a dict
declarative_data_source_dict = declarative_data_source_instance.to_dict()
# create an instance of DeclarativeDataSource from a dict
declarative_data_source_from_dict = DeclarativeDataSource.from_dict(declarative_data_source_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


