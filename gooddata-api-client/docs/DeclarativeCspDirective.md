# DeclarativeCspDirective


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**directive** | **str** |  | 
**sources** | **List[str]** |  | 

## Example

```python
from gooddata_api_client.models.declarative_csp_directive import DeclarativeCspDirective

# TODO update the JSON string below
json = "{}"
# create an instance of DeclarativeCspDirective from a JSON string
declarative_csp_directive_instance = DeclarativeCspDirective.from_json(json)
# print the JSON string representation of the object
print(DeclarativeCspDirective.to_json())

# convert the object into a dict
declarative_csp_directive_dict = declarative_csp_directive_instance.to_dict()
# create an instance of DeclarativeCspDirective from a dict
declarative_csp_directive_from_dict = DeclarativeCspDirective.from_dict(declarative_csp_directive_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


