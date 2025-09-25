# HierarchyObjectIdentification

Represents objects with given ID and type in workspace hierarchy (more than one can exists in different workspaces).

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.hierarchy_object_identification import HierarchyObjectIdentification

# TODO update the JSON string below
json = "{}"
# create an instance of HierarchyObjectIdentification from a JSON string
hierarchy_object_identification_instance = HierarchyObjectIdentification.from_json(json)
# print the JSON string representation of the object
print(HierarchyObjectIdentification.to_json())

# convert the object into a dict
hierarchy_object_identification_dict = hierarchy_object_identification_instance.to_dict()
# create an instance of HierarchyObjectIdentification from a dict
hierarchy_object_identification_from_dict = HierarchyObjectIdentification.from_dict(hierarchy_object_identification_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


