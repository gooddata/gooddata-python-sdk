# DeclarativeDataSource

A data source and its properties.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Data source ID. | 
**name** | **str** | Name of the data source. | 
**type** | **str** | Type of database. | 
**url** | **str** | An connection string relevant to type of database. | 
**schema** | **str** | A scheme/database with the data. | 
**pdm** | [**DeclarativeTables**](DeclarativeTables.md) |  | 
**username** | **str** | User with permission connect the data source/database. | [optional] 
**password** | **str** | Password for the data-source user, property is never returned back. | [optional] 
**token** | **str** | Token as an alternative to username and password. | [optional] 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


