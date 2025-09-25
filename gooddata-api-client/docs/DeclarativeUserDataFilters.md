# DeclarativeUserDataFilters

Declarative form of user data filters.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**user_data_filters** | [**List[DeclarativeUserDataFilter]**](DeclarativeUserDataFilter.md) |  | 

## Example

```python
from gooddata_api_client.models.declarative_user_data_filters import DeclarativeUserDataFilters

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserDataFilters from a JSON string
declarative_user_data_filters_instance = DeclarativeUserDataFilters.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserDataFilters.to_json())

# convert the object into a dict
declarative_user_data_filters_dict = declarative_user_data_filters_instance.to_dict()
# create an instance of DeclarativeUserDataFilters from a dict
declarative_user_data_filters_from_dict = DeclarativeUserDataFilters.from_dict(declarative_user_data_filters_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


