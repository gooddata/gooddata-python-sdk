# JsonApiDataSourceInAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | User-facing name of the data source. | 
**schema** | **str** | The schema to use as the root of the data for the data source. | 
**type** | **str** | Type of the database providing the data for the data source. | 
**cache_strategy** | **str, none_type** | Determines how the results coming from a particular datasource should be cached. | [optional] 
**client_id** | **str, none_type** | The client id to use to connect to the database providing the data for the data source (for example a Databricks Service Account). | [optional] 
**client_secret** | **str, none_type** | The client secret to use to connect to the database providing the data for the data source (for example a Databricks Service Account). | [optional] 
**parameters** | [**[JsonApiDataSourceInAttributesParametersInner], none_type**](JsonApiDataSourceInAttributesParametersInner.md) | Additional parameters to be used when connecting to the database providing the data for the data source. | [optional] 
**password** | **str, none_type** | The password to use to connect to the database providing the data for the data source. | [optional] 
**private_key** | **str, none_type** | The private key to use to connect to the database providing the data for the data source. | [optional] 
**private_key_passphrase** | **str, none_type** | The passphrase used to encrypt the private key. | [optional] 
**token** | **str, none_type** | The token to use to connect to the database providing the data for the data source (for example a BigQuery Service Account). | [optional] 
**url** | **str, none_type** | The URL of the database providing the data for the data source. | [optional] 
**username** | **str, none_type** | The username to use to connect to the database providing the data for the data source. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


