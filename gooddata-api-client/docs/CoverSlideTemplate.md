# CoverSlideTemplate

Settings for cover slide.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**background_image** | **bool** | Show background image on the slide. | [optional] [default to True]
**description_field** | **str** |  | [optional] 
**footer** | [**RunningSection**](RunningSection.md) |  | [optional] 
**header** | [**RunningSection**](RunningSection.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.cover_slide_template import CoverSlideTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of CoverSlideTemplate from a JSON string
cover_slide_template_instance = CoverSlideTemplate.from_json(json)
# print the JSON string representation of the object
print(CoverSlideTemplate.to_json())

# convert the object into a dict
cover_slide_template_dict = cover_slide_template_instance.to_dict()
# create an instance of CoverSlideTemplate from a dict
cover_slide_template_from_dict = CoverSlideTemplate.from_dict(cover_slide_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


