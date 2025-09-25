# JsonApiDataSourceInAttributes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**cache_strategy** | **str** | Determines how the results coming from a particular datasource should be cached. | [optional] 
**client_id** | **str** | The client id to use to connect to the database providing the data for the data source (for example a Databricks Service Account). | [optional] 
**client_secret** | **str** | The client secret to use to connect to the database providing the data for the data source (for example a Databricks Service Account). | [optional] 
**name** | **str** | User-facing name of the data source. | 
**parameters** | [**List[JsonApiDataSourceInAttributesParametersInner]**](JsonApiDataSourceInAttributesParametersInner.md) | Additional parameters to be used when connecting to the database providing the data for the data source. | [optional] 
**password** | **str** | The password to use to connect to the database providing the data for the data source. | [optional] 
**private_key** | **str** | The private key to use to connect to the database providing the data for the data source. | [optional] 
**private_key_passphrase** | **str** | The passphrase used to encrypt the private key. | [optional] 
**var_schema** | **str** | The schema to use as the root of the data for the data source. | 
**token** | **str** | The token to use to connect to the database providing the data for the data source (for example a BigQuery Service Account). | [optional] 
**type** | **str** | Type of the database providing the data for the data source. | 
**url** | **str** | The URL of the database providing the data for the data source. | [optional] 
**username** | **str** | The username to use to connect to the database providing the data for the data source. | [optional] 

## Example

```python
from gooddata_api_client.models.json_api_data_source_in_attributes import JsonApiDataSourceInAttributes

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDataSourceInAttributes from a JSON string
json_api_data_source_in_attributes_instance = JsonApiDataSourceInAttributes.from_json(json)
# print the JSON string representation of the object
print(JsonApiDataSourceInAttributes.to_json())

# convert the object into a dict
json_api_data_source_in_attributes_dict = json_api_data_source_in_attributes_instance.to_dict()
# create an instance of JsonApiDataSourceInAttributes from a dict
json_api_data_source_in_attributes_from_dict = JsonApiDataSourceInAttributes.from_dict(json_api_data_source_in_attributes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


