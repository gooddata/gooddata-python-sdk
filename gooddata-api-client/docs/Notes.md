# Notes


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**note** | [**List[Note]**](Note.md) |  | 

## Example

```python
from gooddata_api_client.models.notes import Notes

# TODO update the JSON string below
json = "{}"
# create an instance of Notes from a JSON string
notes_instance = Notes.from_json(json)
# print the JSON string representation of the object
print(Notes.to_json())

# convert the object into a dict
notes_dict = notes_instance.to_dict()
# create an instance of Notes from a dict
notes_from_dict = Notes.from_dict(notes_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


