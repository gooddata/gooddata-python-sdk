# gooddata_api_client.DataSourceDeclarativeAPIsApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_data_sources_layout**](DataSourceDeclarativeAPIsApi.md#get_data_sources_layout) | **GET** /api/v1/layout/dataSources | Get all data sources
[**put_data_sources_layout**](DataSourceDeclarativeAPIsApi.md#put_data_sources_layout) | **PUT** /api/v1/layout/dataSources | Put all data sources


# **get_data_sources_layout**
> DeclarativeDataSources get_data_sources_layout()

Get all data sources

Retrieve all data sources including related physical model.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_declarative_apis_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
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

### Return type

[**DeclarativeDataSources**](DeclarativeDataSources.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Retrieved all data sources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **put_data_sources_layout**
> put_data_sources_layout(declarative_data_sources)

Put all data sources

Set all data sources including related physical model.

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_declarative_apis_api
from gooddata_api_client.model.declarative_data_sources import DeclarativeDataSources
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_declarative_apis_api.DataSourceDeclarativeAPIsApi(api_client)
    declarative_data_sources = DeclarativeDataSources(
        data_sources=[
            DeclarativeDataSource(
                authentication_type="USERNAME_PASSWORD",
                cache_strategy="ALWAYS",
                client_id="client1234",
                client_secret="client_secret_example",
                decoded_parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                id="pg_local_docker-demo",
                name="postgres demo",
                parameters=[
                    Parameter(
                        name="name_example",
                        value="value_example",
                    ),
                ],
                password="*****",
                permissions=[
                    DeclarativeDataSourcePermission(
                        assignee=AssigneeIdentifier(
                            id="id_example",
                            type="user",
                        ),
                        name="MANAGE",
                    ),
                ],
                private_key="private_key_example",
                private_key_passphrase="private_key_passphrase_example",
                schema="demo",
                token="Bigquery service account JSON. Encode it using base64!",
                type="POSTGRESQL",
                url="jdbc:postgresql://postgres:5432/gooddata",
                username="demo",
            ),
        ],
    ) # DeclarativeDataSources | 

    # example passing only required values which don't have defaults set
    try:
        # Put all data sources
        api_instance.put_data_sources_layout(declarative_data_sources)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceDeclarativeAPIsApi->put_data_sources_layout: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **declarative_data_sources** | [**DeclarativeDataSources**](DeclarativeDataSources.md)|  |

### Return type

void (empty response body)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: Not defined


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**204** | Defined all data sources. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

