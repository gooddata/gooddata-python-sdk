<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.datasets_api.DatasetsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_all_entities_datasets**](#get_all_entities_datasets) | **get** /api/v1/entities/workspaces/{workspaceId}/datasets | Get all Datasets
[**get_entity_datasets**](#get_entity_datasets) | **get** /api/v1/entities/workspaces/{workspaceId}/datasets/{objectId} | Get a Dataset

# **get_all_entities_datasets**
<a id="get_all_entities_datasets"></a>
> JsonApiDatasetOutList get_all_entities_datasets(workspace_id)

Get all Datasets

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import datasets_api
from gooddata_api_client.model.json_api_dataset_out_list import JsonApiDatasetOutList
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get all Datasets
        api_response = api_instance.get_all_entities_datasets(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DatasetsApi->get_all_entities_datasets: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
    }
    query_params = {
        'origin': "ALL",
        'filter': "filter=title==someString;description==someString",
        'include': [
        "include=attributes,facts,references"
    ],
        'page': 0,
        'size': 20,
        'sort': [
        "sort_example"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get all Datasets
        api_response = api_instance.get_all_entities_datasets(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DatasetsApi->get_all_entities_datasets: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
origin | OriginSchema | | optional
filter | FilterSchema | | optional
include | IncludeSchema | | optional
page | PageSchema | | optional
size | SizeSchema | | optional
sort | SortSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# OriginSchema

Defines scope of origin of objects. All by default.

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  | Defines scope of origin of objects. All by default. | must be one of ["ALL", "PARENTS", "NATIVE", ] if omitted the server will use the default value of "ALL"

# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["attributes", "facts", "datasets", "references", "ALL", ] 

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
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_all_entities_datasets.ApiResponseFor200) | Request successfully processed

#### get_all_entities_datasets.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDatasetOutList**](../../models/JsonApiDatasetOutList.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **get_entity_datasets**
<a id="get_entity_datasets"></a>
> JsonApiDatasetOutDocument get_entity_datasets(workspace_idobject_id)

Get a Dataset

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import datasets_api
from gooddata_api_client.model.json_api_dataset_out_document import JsonApiDatasetOutDocument
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = datasets_api.DatasetsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
    }
    header_params = {
    }
    try:
        # Get a Dataset
        api_response = api_instance.get_entity_datasets(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DatasetsApi->get_entity_datasets: %s\n" % e)

    # example passing only optional values
    path_params = {
        'workspaceId': "workspaceId_example",
        'objectId': "objectId_example",
    }
    query_params = {
        'filter': "filter=title==someString;description==someString",
        'include': [
        "include=attributes,facts,references"
    ],
        'metaInclude': [
        "metaInclude=origin,all"
    ],
    }
    header_params = {
        'X-GDC-VALIDATE-RELATIONS': False,
    }
    try:
        # Get a Dataset
        api_response = api_instance.get_entity_datasets(
            path_params=path_params,
            query_params=query_params,
            header_params=header_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DatasetsApi->get_entity_datasets: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
query_params | RequestQueryParams | |
header_params | RequestHeaderParams | |
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/vnd.gooddata.api+json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### query_params
#### RequestQueryParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
filter | FilterSchema | | optional
include | IncludeSchema | | optional
metaInclude | MetaIncludeSchema | | optional


# FilterSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# IncludeSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  |  | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["attributes", "facts", "datasets", "references", "ALL", ] 

# MetaIncludeSchema

Included meta objects

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
list, tuple,  | tuple,  | Included meta objects | 

### Tuple Items
Class Name | Input Type | Accessed Type | Description | Notes
------------- | ------------- | ------------- | ------------- | -------------
items | str,  | str,  |  | must be one of ["origin", "all", "ALL", ] 

### header_params
#### RequestHeaderParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
X-GDC-VALIDATE-RELATIONS | XGDCVALIDATERELATIONSSchema | | optional

# XGDCVALIDATERELATIONSSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
bool,  | BoolClass,  |  | if omitted the server will use the default value of False

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
workspaceId | WorkspaceIdSchema | | 
objectId | ObjectIdSchema | | 

# WorkspaceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

# ObjectIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_entity_datasets.ApiResponseFor200) | Request successfully processed

#### get_entity_datasets.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationVndGooddataApijson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationVndGooddataApijson
Type | Description  | Notes
------------- | ------------- | -------------
[**JsonApiDatasetOutDocument**](../../models/JsonApiDatasetOutDocument.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

