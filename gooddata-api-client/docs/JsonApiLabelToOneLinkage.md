# JsonApiLabelToOneLinkage

References to other resource objects in a to-one (\\\"relationship\\\"). Relationships can be specified by including a member in a resource's links object.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**id** | **str** |  | 
**type** | **str** |  | 

## Example

```python
from gooddata_api_client.models.json_api_label_to_one_linkage import JsonApiLabelToOneLinkage

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiLabelToOneLinkage from a JSON string
json_api_label_to_one_linkage_instance = JsonApiLabelToOneLinkage.from_json(json)
# print the JSON string representation of the object
print(JsonApiLabelToOneLinkage.to_json())

# convert the object into a dict
json_api_label_to_one_linkage_dict = json_api_label_to_one_linkage_instance.to_dict()
# create an instance of JsonApiLabelToOneLinkage from a dict
json_api_label_to_one_linkage_from_dict = JsonApiLabelToOneLinkage.from_dict(json_api_label_to_one_linkage_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


