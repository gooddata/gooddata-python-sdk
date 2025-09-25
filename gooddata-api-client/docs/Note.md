# Note


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**applies_to** | **str** |  | [optional] 
**category** | **str** |  | [optional] 
**content** | **str** |  | [optional] 
**id** | **str** |  | [optional] 
**other_attributes** | **Dict[str, str]** |  | [optional] 
**priority** | **int** |  | [optional] 

## Example

```python
from gooddata_api_client.models.note import Note

# TODO update the JSON string below
json = "{}"
# create an instance of Note from a JSON string
note_instance = Note.from_json(json)
# print the JSON string representation of the object
print(Note.to_json())

# convert the object into a dict
note_dict = note_instance.to_dict()
# create an instance of Note from a dict
note_from_dict = Note.from_dict(note_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


