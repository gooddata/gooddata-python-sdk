# SectionSlideTemplate

Settings for section slide.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**background_image** | **bool** | Show background image on the slide. | [optional] [default to True]
**footer** | [**RunningSection**](RunningSection.md) |  | [optional] 
**header** | [**RunningSection**](RunningSection.md) |  | [optional] 

## Example

```python
from gooddata_api_client.models.section_slide_template import SectionSlideTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of SectionSlideTemplate from a JSON string
section_slide_template_instance = SectionSlideTemplate.from_json(json)
# print the JSON string representation of the object
print(SectionSlideTemplate.to_json())

# convert the object into a dict
section_slide_template_dict = section_slide_template_instance.to_dict()
# create an instance of SectionSlideTemplate from a dict
section_slide_template_from_dict = SectionSlideTemplate.from_dict(section_slide_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


