# DeclarativeDataSources

A data source and its properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data_sources** | [**List[DeclarativeDataSource]**](DeclarativeDataSource.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_data_sources import DeclarativeDataSources

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeDataSources from a JSON string
declarative_data_sources_instance = DeclarativeDataSources.from_json(json)
# print the JSON string representation of the object
print(DeclarativeDataSources.to_json())

# convert the object into a dict
declarative_data_sources_dict = declarative_data_sources_instance.to_dict()
# create an instance of DeclarativeDataSources from a dict
declarative_data_sources_from_dict = DeclarativeDataSources.from_dict(declarative_data_sources_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


