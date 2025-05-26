# DeclarativeDataSource

A data source and its properties.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Data source ID. | 
**name** | **str** | Name of the data source. | 
**schema** | **str** | A scheme/database with the data. | 
**type** | **str** | Type of database. | 
**authentication_type** | **str, none_type** | Type of authentication used to connect to the database. | [optional] 
**cache_strategy** | **str** | Determines how the results coming from a particular datasource should be cached. - ALWAYS: The results from the datasource should be cached normally (the default). - NEVER: The results from the datasource should never be cached. | [optional] 
**client_id** | **str** | Id of client with permission to connect to the data source. | [optional] 
**client_secret** | **str** | The client secret to use to connect to the database providing the data for the data source. | [optional] 
**decoded_parameters** | [**[Parameter]**](Parameter.md) |  | [optional] 
**parameters** | [**[Parameter]**](Parameter.md) |  | [optional] 
**password** | **str** | Password for the data-source user, property is never returned back. | [optional] 
**permissions** | [**[DeclarativeDataSourcePermission]**](DeclarativeDataSourcePermission.md) |  | [optional] 
**private_key** | **str, none_type** | The private key to use to connect to the database providing the data for the data source. | [optional] 
**private_key_passphrase** | **str, none_type** | The passphrase used to encrypt the private key. | [optional] 
**token** | **str** | Token as an alternative to username and password. | [optional] 
**url** | **str** | An connection string relevant to type of database. | [optional] 
**username** | **str** | User with permission connect the data source/database. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


