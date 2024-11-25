# TestRequest

A request containing all information for testing existing data source.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**client_id** | **str** | Id for client based authentication for data sources which supports it. | [optional] 
**client_secret** | **str** | Secret for client based authentication for data sources which supports it. | [optional] 
**parameters** | [**[DataSourceParameter]**](DataSourceParameter.md) |  | [optional] 
**password** | **str** | Database user password. | [optional] 
**private_key** | **str** | Private key for data sources which supports key-pair authentication. | [optional] 
**private_key_passphrase** | **str** | Passphrase for a encrypted version of a private key. | [optional] 
**schema** | **str** | Database schema. | [optional] 
**token** | **str** | Secret for token based authentication for data sources which supports it. | [optional] 
**url** | **str** | URL to database in JDBC format, where test should connect to. | [optional] 
**username** | **str** | Database user name. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


