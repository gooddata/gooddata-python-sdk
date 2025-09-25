# ObjectLinksContainer


## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**links** | [**ObjectLinks**](ObjectLinks.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.object_links_container import ObjectLinksContainer

# TODO update the JSON string below
json = "{}"
# create an instance of ObjectLinksContainer from a JSON string
object_links_container_instance = ObjectLinksContainer.from_json(json)
# print the JSON string representation of the object
print(ObjectLinksContainer.to_json())

# convert the object into a dict
object_links_container_dict = object_links_container_instance.to_dict()
# create an instance of ObjectLinksContainer from a dict
object_links_container_from_dict = ObjectLinksContainer.from_dict(object_links_container_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


