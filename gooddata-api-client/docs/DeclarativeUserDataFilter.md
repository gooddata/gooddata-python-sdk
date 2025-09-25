# DeclarativeUserDataFilter

User Data Filters serving the filtering of what data users can see in workspaces.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description** | **str** | User Data Filters setting description. | [optional] 
**id** | **str** | User Data Filters ID. This ID is further used to refer to this instance. | 
**maql** | **str** | Expression in MAQL specifying the User Data Filter | 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | User Data Filters setting title. | 
**user** | [**DeclarativeUserIdentifier**](DeclarativeUserIdentifier.md) |  | [optional] 
**user_group** | [**DeclarativeUserGroupIdentifier**](DeclarativeUserGroupIdentifier.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.declarative_user_data_filter import DeclarativeUserDataFilter

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeUserDataFilter from a JSON string
declarative_user_data_filter_instance = DeclarativeUserDataFilter.from_json(json)
# print the JSON string representation of the object
print(DeclarativeUserDataFilter.to_json())

# convert the object into a dict
declarative_user_data_filter_dict = declarative_user_data_filter_instance.to_dict()
# create an instance of DeclarativeUserDataFilter from a dict
declarative_user_data_filter_from_dict = DeclarativeUserDataFilter.from_dict(declarative_user_data_filter_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


