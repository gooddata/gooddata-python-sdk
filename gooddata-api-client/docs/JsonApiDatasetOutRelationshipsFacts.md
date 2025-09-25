# JsonApiDatasetOutRelationshipsFacts


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**data** | [**List[JsonApiFactLinkage]**](JsonApiFactLinkage.md) | References to other resource objects in a to-many (\\\&quot;relationship\\\&quot;). Relationships can be specified by including a member in a resource&#39;s links object. | 

## Example

```python
from gooddata_api_client.models.json_api_dataset_out_relationships_facts import JsonApiDatasetOutRelationshipsFacts

# TODO update the JSON string below
json = "{}"
# create an instance of JsonApiDatasetOutRelationshipsFacts from a JSON string
json_api_dataset_out_relationships_facts_instance = JsonApiDatasetOutRelationshipsFacts.from_json(json)
# print the JSON string representation of the object
print(JsonApiDatasetOutRelationshipsFacts.to_json())

# convert the object into a dict
json_api_dataset_out_relationships_facts_dict = json_api_dataset_out_relationships_facts_instance.to_dict()
# create an instance of JsonApiDatasetOutRelationshipsFacts from a dict
json_api_dataset_out_relationships_facts_from_dict = JsonApiDatasetOutRelationshipsFacts.from_dict(json_api_dataset_out_relationships_facts_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


