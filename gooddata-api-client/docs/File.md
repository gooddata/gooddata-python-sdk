# File


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**any** | **List[object]** |  | [optional] 
**can_resegment** | **str** |  | [optional] 
**id** | **str** |  | [optional] 
**notes** | [**Notes**](Notes.md) |  | [optional] 
**original** | **str** |  | [optional] 
**other_attributes** | **Dict[str, str]** |  | [optional] 
**skeleton** | [**Skeleton**](Skeleton.md) |  | [optional] 
**space** | **str** |  | [optional] 
**src_dir** | **str** |  | [optional] 
**translate** | **str** |  | [optional] 
**trg_dir** | **str** |  | [optional] 
**unit_or_group** | **List[object]** |  | [optional] 

## Example

```python
from gooddata_api_client.models.file import File

# TODO update the JSON string below
json = "{}"
# create an instance of File from a JSON string
file_instance = File.from_json(json)
# print the JSON string representation of the object
print(File.to_json())

# convert the object into a dict
file_dict = file_instance.to_dict()
# create an instance of File from a dict
file_from_dict = File.from_dict(file_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


