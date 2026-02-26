<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.export_templates_api.ExportTemplatesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**create_entity_export_templates**](#create_entity_export_templates) | **post** /api/v1/entities/exportTemplates | Post Export Template entities
[**delete_entity_export_templates**](#delete_entity_export_templates) | **delete** /api/v1/entities/exportTemplates/{id} | Delete Export Template entity
[**get_all_entities_export_templates**](#get_all_entities_export_templates) | **get** /api/v1/entities/exportTemplates | GET all Export Template entities
[**get_entity_export_templates**](#get_entity_export_templates) | **get** /api/v1/entities/exportTemplates/{id} | GET Export Template entity
[**patch_entity_export_templates**](#patch_entity_export_templates) | **patch** /api/v1/entities/exportTemplates/{id} | Patch Export Template entity
[**update_entity_export_templates**](#update_entity_export_templates) | **put** /api/v1/entities/exportTemplates/{id} | PUT Export Template entity

# **create_entity_export_templates**
<a id="create_entity_export_templates"></a>
> JsonApiExportTemplateOutDocument create_entity_export_templates(json_api_export_template_post_optional_id_document)

Post Export Template entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import export_templates_api
from gooddata_api_client.model.json_api_export_template_post_optional_id_document import JsonApiExportTemplatePostOptionalIdDocument
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)

    # example passing only required values which don't have defaults set
    body = JsonApiExportTemplatePostOptionalIdDocument(
        data=JsonApiExportTemplatePostOptionalId(
            attributes=dict(
                dashboard_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
,
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field="About:\n{{dashboardDescription}}\n\n{{dashboardFilters}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                ),
                name="name_example",
                widget_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    )
    try:
        # Post Export Template entities
        api_response = api_instance.create_entity_export_templates(
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->create_entity_export_templates: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplatePostOptionalIdDocument**](../../models/JsonApiExportTemplatePostOptionalIdDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplatePostOptionalIdDocument**](../../models/JsonApiExportTemplatePostOptionalIdDocument.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
201 | [ApiResponseFor201](#create_entity_export_templates.ApiResponseFor201) | Request successfully processed

#### create_entity_export_templates.ApiResponseFor201
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor201ResponseBodyApplicationJson, SchemaFor201ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor201ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


# SchemaFor201ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **delete_entity_export_templates**
<a id="delete_entity_export_templates"></a>
> delete_entity_export_templates(id)

Delete Export Template entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import export_templates_api
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # Delete Export Template entity
        api_response = api_instance.delete_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->delete_entity_export_templates: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue",
    }
    try:
        # Delete Export Template entity
        api_response = api_instance.delete_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->delete_entity_export_templates: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#delete_entity_export_templates.ApiResponseFor204) | Successfully deleted

#### delete_entity_export_templates.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_all_entities_export_templates**
<a id="get_all_entities_export_templates"></a>
> JsonApiExportTemplateOutList get_all_entities_export_templates()

GET all Export Template entities

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import export_templates_api
from gooddata_api_client.model.json_api_export_template_out_list import JsonApiExportTemplateOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)

    # example passing only optional values
    query_params = {
        'filter': "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue",
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=page,all"
    ],
    }
    try:
        # GET all Export Template entities
        api_response = api_instance.get_all_entities_export_templates(
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->get_all_entities_export_templates: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# PageSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 0

# SizeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
decimal.Decimal, int,  | decimal.Decimal,  |  | if omitted the server will use the default value of 20

# SortSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["page", "all", "ALL", ] 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_export_templates.ApiResponseFor200) | Request successfully processed

#### get_all_entities_export_templates.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutList**](../../models/JsonApiExportTemplateOutList.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutList**](../../models/JsonApiExportTemplateOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_export_templates**
<a id="get_entity_export_templates"></a>
> JsonApiExportTemplateOutDocument get_entity_export_templates(id)

GET Export Template entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import export_templates_api
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    try:
        # GET Export Template entity
        api_response = api_instance.get_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->get_entity_export_templates: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue",
    }
    try:
        # GET Export Template entity
        api_response = api_instance.get_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->get_entity_export_templates: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_export_templates.ApiResponseFor200) | Request successfully processed

#### get_entity_export_templates.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **patch_entity_export_templates**
<a id="patch_entity_export_templates"></a>
> JsonApiExportTemplateOutDocument patch_entity_export_templates(idjson_api_export_template_patch_document)

Patch Export Template entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import export_templates_api
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from gooddata_api_client.model.json_api_export_template_patch_document import JsonApiExportTemplatePatchDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiExportTemplatePatchDocument(
        data=JsonApiExportTemplatePatch(
            attributes=dict(
                dashboard_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
,
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field="About:\n{{dashboardDescription}}\n\n{{dashboardFilters}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                ),
                name="name_example",
                widget_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    )
    try:
        # Patch Export Template entity
        api_response = api_instance.patch_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->patch_entity_export_templates: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue",
    }
    body = JsonApiExportTemplatePatchDocument(
        data=JsonApiExportTemplatePatch(
            attributes=dict(
                dashboard_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
,
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field="About:\n{{dashboardDescription}}\n\n{{dashboardFilters}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                ),
                name="name_example",
                widget_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    )
    try:
        # Patch Export Template entity
        api_response = api_instance.patch_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->patch_entity_export_templates: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplatePatchDocument**](../../models/JsonApiExportTemplatePatchDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplatePatchDocument**](../../models/JsonApiExportTemplatePatchDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#patch_entity_export_templates.ApiResponseFor200) | Request successfully processed

#### patch_entity_export_templates.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **update_entity_export_templates**
<a id="update_entity_export_templates"></a>
> JsonApiExportTemplateOutDocument update_entity_export_templates(idjson_api_export_template_in_document)

PUT Export Template entity

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import export_templates_api
from gooddata_api_client.model.json_api_export_template_in_document import JsonApiExportTemplateInDocument
from gooddata_api_client.model.json_api_export_template_out_document import JsonApiExportTemplateOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = export_templates_api.ExportTemplatesApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
    }
    body = JsonApiExportTemplateInDocument(
        data=JsonApiExportTemplateIn(
            attributes=dict(
                dashboard_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
,
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field="About:\n{{dashboardDescription}}\n\n{{dashboardFilters}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                ),
                name="name_example",
                widget_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    )
    try:
        # PUT Export Template entity
        api_response = api_instance.update_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->update_entity_export_templates: %s\n" % e)

    # example passing only optional values
    path_params = {
        'id': "/6bUUGjjNSwg0_bs",
    }
    query_params = {
        'filter': "name==someString;dashboardSlidesTemplate==DashboardSlidesTemplateValue",
    }
    body = JsonApiExportTemplateInDocument(
        data=JsonApiExportTemplateIn(
            attributes=dict(
                dashboard_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(
                        description_field="{{dashboardFilters}}",
                        footer=RunningSection(
                            left="left_example",
                            right="right_example",
                        ),
,
                    ),
                    cover_slide=CoverSlideTemplate(
                        background_image=True,
                        description_field="Exported at: {{exportedAt}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                    intro_slide=IntroSlideTemplate(
                        background_image=True,
                        description_field="About:\n{{dashboardDescription}}\n\n{{dashboardFilters}}",
                        footer=RunningSection(),
                        header=RunningSection(),
                        title_field="Introduction",
                    ),
                    section_slide=SectionSlideTemplate(
                        background_image=True,
                        footer=RunningSection(),
                        header=RunningSection(),
                    ),
                ),
                name="name_example",
                widget_slides_template=dict(
                    applied_on=["PDF","PPTX"],
                    content_slide=ContentSlideTemplate(),
                ),
            ),
            id="id1",
            type="exportTemplate",
        ),
    )
    try:
        # PUT Export Template entity
        api_response = api_instance.update_entity_export_templates(
            path_params=path_params,
            query_params=query_params,
            body=body,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling ExportTemplatesApi->update_entity_export_templates: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson, SchemaForRequestBodyApplicationVndGooddataApijson] | required |
query_params | RequestQueryParams | |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
accept_content_types | typing.Tuple[str] | default is ('application/json', 'application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateInDocument**](../../models/JsonApiExportTemplateInDocument.md) |  | 


# SchemaForRequestBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateInDocument**](../../models/JsonApiExportTemplateInDocument.md) |  | 


### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
id | IdSchema | | 

# IdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#update_entity_export_templates.ApiResponseFor200) | Request successfully processed

#### update_entity_export_templates.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiExportTemplateOutDocument**](../../models/JsonApiExportTemplateOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

