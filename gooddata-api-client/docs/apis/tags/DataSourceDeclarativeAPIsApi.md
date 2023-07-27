<a id="__pageTop"></a>
# gooddata_api_client.apis.tags.data_source_declarative_apis_api.DataSourceDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_sources_layout**](#get_data_sources_layout) | **get** /api/v1/layout/dataSources | Get all data sources
[**put_data_sources_layout**](#put_data_sources_layout) | **put** /api/v1/layout/dataSources | Put all data sources

# **get_data_sources_layout**
<a id="get_data_sources_layout"></a>
> DeclarativeDataSources get_data_sources_layout()

Get all data sources

Retrieve all data sources including related physical model.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_declarative_apis_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_declarative_apis_api.DataSourceDeclarativeAPIsApi(api_client)

    # example, this endpoint has no required or optional parameters
    try:
        # Get all data sources
        api_response = api_instance.get_data_sources_layout()
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceDeclarativeAPIsApi->get_data_sources_layout: %s\n" % e)
```
### Parameters
This endpoint does not need any parameter.

### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#get_data_sources_layout.ApiResponseFor200) | Retrieved all data sources.

#### get_data_sources_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | typing.Union[SchemaFor200ResponseBodyApplicationJson, ] |  |
headers | Unset | headers were not defined |

# SchemaFor200ResponseBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeDataSources**](../../models/DeclarativeDataSources.md) |  | 


### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

# **put_data_sources_layout**
<a id="put_data_sources_layout"></a>
> put_data_sources_layout(declarative_data_sources)

Put all data sources

Set all data sources including related physical model.

### Example

```python
import gooddata_api_client
from gooddata_api_client.apis.tags import data_source_declarative_apis_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)

# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient(configuration) as api_client:
    # Create an instance of the API class
    api_instance = data_source_declarative_apis_api.DataSourceDeclarativeAPIsApi(api_client)

    # example passing only required values which don't have defaults set
    body = DeclarativeDataSources(
        data_sources=[
            DeclarativeDataSource(
                cache_path=[
                    "[ \"dfs\", \"data\" ]. Example used in Apache Drill."
                ],
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    )
                ],
                enable_caching=False,
                id="pg_local_docker-demo",
                name="postgres demo",
,
                password="*****",
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
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    )
                ],
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            )
        ],
    )
    try:
        # Put all data sources
        api_response = api_instance.put_data_sources_layout(
            body=body,
        )
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceDeclarativeAPIsApi->put_data_sources_layout: %s\n" % e)
```
### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
body | typing.Union[SchemaForRequestBodyApplicationJson] | required |
content_type | str | optional, default is 'application/json' | Selects the schema and serialization of the request body
stream | bool | default is False | if True then the response.content will be streamed and loaded from a file like object. When downloading a file, set this to True to force the code to deserialize the content to a FileSchema file
timeout | typing.Optional[typing.Union[int, typing.Tuple]] | default is None | the timeout used by the rest client
skip_deserialization | bool | default is False | when True, headers and body will be unset and an instance of api_client.ApiResponseWithoutDeserialization will be returned

### body

# SchemaForRequestBodyApplicationJson
Type | Description  | Notes
------------- | ------------- | -------------
[**DeclarativeDataSources**](../../models/DeclarativeDataSources.md) |  | 


### Return Types, Responses

Code | Class | Description
------------- | ------------- | -------------
n/a | api_client.ApiResponseWithoutDeserialization | When skip_deserialization is True this response is returned
200 | [ApiResponseFor200](#put_data_sources_layout.ApiResponseFor200) | Defined all data sources.

#### put_data_sources_layout.ApiResponseFor200
Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
response | urllib3.HTTPResponse | Raw response |
body | Unset | body was not defined |
headers | Unset | headers were not defined |

### Authorization

No authorization required

[[Back to top]](#__pageTop) [[Back to API list]](../../../README.md#documentation-for-api-endpoints) [[Back to Model list]](../../../README.md#documentation-for-models) [[Back to README]](../../../README.md)

