# gooddata_afm_client.ElementsControllerApi

All URIs are relative to *https://staging.anywhere.gooddata.com*

Method | HTTP request | Description
------------- | ------------- | -------------
[**compute_label_elements**](ElementsControllerApi.md#compute_label_elements) | **GET** /api/actions/workspaces/{workspaceId}/execution/collectLabelElements | Listing of label values.


# **compute_label_elements**
> ElementsResponse compute_label_elements(workspace_id, label)

Listing of label values.

Returns paged list of elements (values) of given label satisfying given filtering criteria.

### Example

```python
import time
import gooddata_afm_client
from gooddata_afm_client.api import elements_controller_api
from gooddata_afm_client.model.elements_response import ElementsResponse
from pprint import pprint
# Defining the host is optional and defaults to https://staging.anywhere.gooddata.com
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_afm_client.Configuration(
    host = "https://staging.anywhere.gooddata.com"
)


# Enter a context with an instance of the API client
with gooddata_afm_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = elements_controller_api.ElementsControllerApi(api_client)
    workspace_id = "26bUUGjjNSwg0_bs9ZayIMrKdgNvb6gvxmPb9GcsM61ate1RA89q3w1l4eH4XxEz.5awxoFZxHzs6ED.kjUSnTINkYPUndNl8pmPg5K897Fu1JEFj9R1_dz9rEoBi0LnU8SsOWJ7wYrcziVQdt8mVLxbg4bCLrLBcmXxWQK6MzKSg5jphei0IfRRwpnT_Z.qKa_YppZepezJ0.VmLSUTLYyW" # str | Workspace identifier
    label = "label_example" # str | Requested label.
    sort_order = "ASC" # str | Sort order of returned items. Items are sorted by ```label``` title. (optional) if omitted the server will use the default value of "ASC"
    include_total_without_filters = False # bool | Specify if ```totalCountWithoutFilters``` should be returned. (optional) if omitted the server will use the default value of False
    complement_filter = False # bool | Inverse filter: * ```false``` - return items matching ```patternFilter``` * ```true``` - return items not matching ```patternFilter``` (optional) if omitted the server will use the default value of False
    pattern_filter = "patternFilter_example" # str | Return only items, whose ```label``` title case insensitively contains ```filter``` as substring. (optional)
    offset = 0 # int | Request page with this offset. (optional) if omitted the server will use the default value of 0
    limit = 1000 # int | Return only this number of items. (optional) if omitted the server will use the default value of 1000
    data_sampling_percentage = 0 # float | Specifies the percentage of rows from fact datasets to use during computation. This feature is available only for workspaces that use a Vertica Data Source without table views. (optional)
    skip_cache = True # bool | Ignore all caches during execution of current request. (optional)

    # example passing only required values which don't have defaults set
    try:
        # Listing of label values.
        api_response = api_instance.compute_label_elements(workspace_id, label)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ElementsControllerApi->compute_label_elements: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Listing of label values.
        api_response = api_instance.compute_label_elements(workspace_id, label, sort_order=sort_order, include_total_without_filters=include_total_without_filters, complement_filter=complement_filter, pattern_filter=pattern_filter, offset=offset, limit=limit, data_sampling_percentage=data_sampling_percentage, skip_cache=skip_cache)
        pprint(api_response)
    except gooddata_afm_client.ApiException as e:
        print("Exception when calling ElementsControllerApi->compute_label_elements: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **workspace_id** | **str**| Workspace identifier |
 **label** | **str**| Requested label. |
 **sort_order** | **str**| Sort order of returned items. Items are sorted by &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title. | [optional] if omitted the server will use the default value of "ASC"
 **include_total_without_filters** | **bool**| Specify if &#x60;&#x60;&#x60;totalCountWithoutFilters&#x60;&#x60;&#x60; should be returned. | [optional] if omitted the server will use the default value of False
 **complement_filter** | **bool**| Inverse filter: * &#x60;&#x60;&#x60;false&#x60;&#x60;&#x60; - return items matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; * &#x60;&#x60;&#x60;true&#x60;&#x60;&#x60; - return items not matching &#x60;&#x60;&#x60;patternFilter&#x60;&#x60;&#x60; | [optional] if omitted the server will use the default value of False
 **pattern_filter** | **str**| Return only items, whose &#x60;&#x60;&#x60;label&#x60;&#x60;&#x60; title case insensitively contains &#x60;&#x60;&#x60;filter&#x60;&#x60;&#x60; as substring. | [optional]
 **offset** | **int**| Request page with this offset. | [optional] if omitted the server will use the default value of 0
 **limit** | **int**| Return only this number of items. | [optional] if omitted the server will use the default value of 1000
 **data_sampling_percentage** | **float**| Specifies the percentage of rows from fact datasets to use during computation. This feature is available only for workspaces that use a Vertica Data Source without table views. | [optional]
 **skip_cache** | **bool**| Ignore all caches during execution of current request. | [optional]

### Return type

[**ElementsResponse**](ElementsResponse.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details
| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | List of label values. |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

