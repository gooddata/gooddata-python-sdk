# IntroSlideTemplate

Settings for intro slide.

## Properties

Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**background_image** | **bool** | Show background image on the slide. | [optional] [default to True]
**description_field** | **str** |  | [optional] 
**footer** | [**RunningSection**](RunningSection.md) |  | [optional] 
**header** | [**RunningSection**](RunningSection.md) |  | [optional] 
**title_field** | **str** |  | [optional] 

## Example

```python
from gooddata_api_client.models.intro_slide_template import IntroSlideTemplate

# TODO update the JSON string below
json = "{}"
# create an instance of IntroSlideTemplate from a JSON string
intro_slide_template_instance = IntroSlideTemplate.from_json(json)
# print the JSON string representation of the object
print(IntroSlideTemplate.to_json())

# convert the object into a dict
intro_slide_template_dict = intro_slide_template_instance.to_dict()
# create an instance of IntroSlideTemplate from a dict
intro_slide_template_from_dict = IntroSlideTemplate.from_dict(intro_slide_template_dict)
```
[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


