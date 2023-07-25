<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.pdm_declarative_apis_api.PDMDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_pdm_layout**](#get_pdm_layout) | **get** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Get data source physical model layout
[**set_pdm_layout**](#set_pdm_layout) | **put** /api/v1/layout/dataSources/{dataSourceId}/physicalModel | Set data source physical model layout

# **get_pdm_layout**
<a id="get_pdm_layout"></a>
> DeclarativePdm get_pdm_layout(data_source_id)

Get data source physical model layout

Retrieve complete layout of tables with their columns

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import pdm_declarative_apis_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pdm_declarative_apis_api.PDMDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    try:
        # Get data source physical model layout
        api_response = api_instance.get_pdm_layout(
            path_params=path_params,
        )
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PDMDeclarativeAPIsApi->get_pdm_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
path_params | RequestPathParams | |
accept_content_types | typing.Tuple[str] | default is ('application/json', ) | Tells the server the content type(s) that are accepted by the client
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
dataSourceId | DataSourceIdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_pdm_layout.ApiResponseFor200) | Retrieved data source physical mode layout.

#### get_pdm_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativePdm**](../../models/DeclarativePdm.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **set_pdm_layout**
<a id="set_pdm_layout"></a>
> set_pdm_layout(data_source_iddeclarative_pdm)

Set data source physical model layout

Sets complete layout of tables with their columns under corresponding Data Source.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import pdm_declarative_apis_api
from gooddata_api_client.model.declarative_pdm import DeclarativePdm
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = pdm_declarative_apis_api.PDMDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    path_params = {
        'dataSourceId': "dataSourceId_example",
    }
    body = DeclarativePdm(
        pdm=DeclarativeTables(
            tables=[
                DeclarativeTable(
                    columns=[
                        DeclarativeColumn(
                            data_type="INT",
                            is_primary_key=True,
                            name="customer_id",
                            referenced_table_column="customer_id",
                            referenced_table_id="customers",
                        )
                    ],
                    id="customers",
                    name_prefix="out_gooddata",
                    path=["table_schema","table_name"],
                    type="VIEW",
                )
            ],
        ),
    )
    try:
        # Set data source physical model layout
        api_response = api_instance.set_pdm_layout(
            path_params=path_params,
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling PDMDeclarativeAPIsApi->set_pdm_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
path_params | RequestPathParams | |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativePdm**](../../models/DeclarativePdm.md) |  | 


### path_params
#### RequestPathParams

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
dataSourceId | DataSourceIdSchema | | 

# DataSourceIdSchema

## Model Type Info
Input Type | Accessed Type | Description | Notes
------------ | ------------- | ------------- | -------------
str,  | str,  |  | 

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
204 | [ApiResponseFor204](#set_pdm_layout.ApiResponseFor204) | Data source physical mode layout set successfully.

#### set_pdm_layout.ApiResponseFor204
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

