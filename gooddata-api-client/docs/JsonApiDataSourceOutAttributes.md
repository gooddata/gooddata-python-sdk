# JsonApiDataSourceOutAttributes


## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**name** | **str** | User-facing name of the data source. | 
**schema** | **str** | The schema to use as the root of the data for the data source. | 
**type** | **str** | Type of the database providing the data for the data source. | 
**authentication_type** | **str, none_type** | Type of authentication used to connect to the database. | [optional] 
**cache_strategy** | **str, none_type** | Determines how the results coming from a particular datasource should be cached. | [optional] 
**client_id** | **str, none_type** | The client id to use to connect to the database providing the data for the data source (for example a Databricks Service Account). | [optional] 
**decoded_parameters** | [**[JsonApiDataSourceInAttributesParametersInner], none_type**](JsonApiDataSourceInAttributesParametersInner.md) | Decoded parameters to be used when connecting to the database providing the data for the data source. | [optional] 
**parameters** | [**[JsonApiDataSourceInAttributesParametersInner], none_type**](JsonApiDataSourceInAttributesParametersInner.md) | Additional parameters to be used when connecting to the database providing the data for the data source. | [optional] 
**url** | **str, none_type** | The URL of the database providing the data for the data source. | [optional] 
**username** | **str, none_type** | The username to use to connect to the database providing the data for the data source. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


