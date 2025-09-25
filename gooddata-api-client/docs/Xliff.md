# Xliff


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**file** | [**List[File]**](File.md) |  | 
**other_attributes** | **Dict[str, str]** |  | [optional] 
**space** | **str** |  | [optional] 
**src_lang** | **str** |  | [optional] 
**trg_lang** | **str** |  | [optional] 
**version** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.xliff import Xliff

# TODO update the JSON string below
json = "{}"
# create an instance of Xliff from a JSON string
xliff_instance = Xliff.from_json(json)
# print the JSON string representation of the object
print(Xliff.to_json())

# convert the object into a dict
xliff_dict = xliff_instance.to_dict()
# create an instance of Xliff from a dict
xliff_from_dict = Xliff.from_dict(xliff_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


