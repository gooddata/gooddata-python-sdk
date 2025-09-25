# DeclarativeTheme

Theme and its properties.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | 
**id** | **str** |  | 
**name** | **str** |  | 

## Example

```python
from gooddata_api_client.models.declarative_theme import DeclarativeTheme

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeTheme from a JSON string
declarative_theme_instance = DeclarativeTheme.from_json(json)
# print the JSON string representation of the object
print(DeclarativeTheme.to_json())

# convert the object into a dict
declarative_theme_dict = declarative_theme_instance.to_dict()
# create an instance of DeclarativeTheme from a dict
declarative_theme_from_dict = DeclarativeTheme.from_dict(declarative_theme_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


