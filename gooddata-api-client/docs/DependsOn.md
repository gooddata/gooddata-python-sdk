# DependsOn

Filter definition type specified by label and values.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**complement_filter** | **bool** | Inverse filtering mode. | [optional] [default to False]
**label** | **str** | Specifies on which label the filter depends on. | 
**values** | **List[Optional[str]]** | Specifies values of the label for element filtering. | 

## Example

```python
from gooddata_api_client.models.depends_on import DependsOn

# TODO update the JSON string below
json = "{}"
# create an instance of DependsOn from a JSON string
depends_on_instance = DependsOn.from_json(json)
# print the JSON string representation of the object
print(DependsOn.to_json())

# convert the object into a dict
depends_on_dict = depends_on_instance.to_dict()
# create an instance of DependsOn from a dict
depends_on_from_dict = DependsOn.from_dict(depends_on_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


