# DeclarativeFilterContext


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**content** | **object** | Free-form JSON object | 
**description** | **str** | Filter Context description. | [optional] 
**id** | **str** | Filter Context ID. | 
**tags** | **List[str]** | A list of tags. | [optional] 
**title** | **str** | Filter Context title. | 

## Example

```python
from gooddata_api_client.models.declarative_filter_context import DeclarativeFilterContext

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeFilterContext from a JSON string
declarative_filter_context_instance = DeclarativeFilterContext.from_json(json)
# print the JSON string representation of the object
print(DeclarativeFilterContext.to_json())

# convert the object into a dict
declarative_filter_context_dict = declarative_filter_context_instance.to_dict()
# create an instance of DeclarativeFilterContext from a dict
declarative_filter_context_from_dict = DeclarativeFilterContext.from_dict(declarative_filter_context_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


