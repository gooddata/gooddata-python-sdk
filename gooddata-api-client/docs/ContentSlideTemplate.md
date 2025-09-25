# ContentSlideTemplate

Settings for content slide.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**description_field** | **str** |  | [optional] 
**footer** | [**RunningSection**](RunningSection.md) |  | [optional] 
**header** | [**RunningSection**](RunningSection.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.content_slide_template import ContentSlideTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of ContentSlideTemplate from a JSON string
content_slide_template_instance = ContentSlideTemplate.from_json(json)
# print the JSON string representation of the object
print(ContentSlideTemplate.to_json())

# convert the object into a dict
content_slide_template_dict = content_slide_template_instance.to_dict()
# create an instance of ContentSlideTemplate from a dict
content_slide_template_from_dict = ContentSlideTemplate.from_dict(content_slide_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


