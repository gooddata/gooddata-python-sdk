# gooddata_api_client.DataSourceFilesAnalysisApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**analyze_csv**](DataSourceFilesAnalysisApi.md#analyze_csv) | **POST** /api/v1/actions/fileStorage/staging/analyzeCsv | Analyze CSV


# **analyze_csv**
> [AnalyzeCsvResponse] analyze_csv(analyze_csv_request)

Analyze CSV

Analyzes CSV files at the given locations

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import data_source_files_analysis_api
from gooddata_api_client.model.analyze_csv_response import AnalyzeCsvResponse
from gooddata_api_client.model.analyze_csv_request import AnalyzeCsvRequest
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = data_source_files_analysis_api.DataSourceFilesAnalysisApi(api_client)
    analyze_csv_request = AnalyzeCsvRequest(
        analyze_requests=[
            AnalyzeCsvRequestItem(
                config=AnalyzeCsvRequestItemConfig(
                    delimiters=[
                        "delimiters_example",
                    ],
                    header_detect_max_rows=1,
                    header_row_count=1,
                    result_rows=1,
                ),
                location="location_example",
            ),
        ],
    ) # AnalyzeCsvRequest | 

    # example passing only required values which don't have defaults set
    try:
        # Analyze CSV
        api_response = api_instance.analyze_csv(analyze_csv_request)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling DataSourceFilesAnalysisApi->analyze_csv: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **analyze_csv_request** | [**AnalyzeCsvRequest**](AnalyzeCsvRequest.md)|  |

### Return type

[**[AnalyzeCsvResponse]**](AnalyzeCsvResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: application/json
 - **Accept**: application/json


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Successful analysis. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

