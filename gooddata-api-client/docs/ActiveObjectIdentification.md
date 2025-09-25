# ActiveObjectIdentification

Object, with which the user is actively working.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** | Object ID. | 
**type** | **str** | Object type, e.g. dashboard. | 
**workspace_id** | **str** | Workspace ID. | 

## Example

```python
from gooddata_api_client.models.active_object_identification import ActiveObjectIdentification

# TODO update the JSON string below
json = "{}"
# create an instance of ActiveObjectIdentification from a JSON string
active_object_identification_instance = ActiveObjectIdentification.from_json(json)
# print the JSON string representation of the object
print(ActiveObjectIdentification.to_json())

# convert the object into a dict
active_object_identification_dict = active_object_identification_instance.to_dict()
# create an instance of ActiveObjectIdentification from a dict
active_object_identification_from_dict = ActiveObjectIdentification.from_dict(active_object_identification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


