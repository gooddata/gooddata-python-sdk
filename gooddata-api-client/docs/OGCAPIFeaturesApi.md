# gooddata_api_client.OGCAPIFeaturesApi

All URIs are relative to *http://localhost*

Method | HTTP request | Description
------------- | ------------- | -------------
[**get_collection_items**](OGCAPIFeaturesApi.md#get_collection_items) | **GET** /api/v1/location/collections/{collectionId}/items | Get collection features
[**get_custom_collection_items**](OGCAPIFeaturesApi.md#get_custom_collection_items) | **GET** /api/v1/location/custom/collections/{collectionId}/items | Get custom collection features


# **get_collection_items**
> GeoJsonFeatureCollection get_collection_items(collection_id)

Get collection features

Retrieve features from a GeoCollections collection as GeoJSON

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ogcapi_features_api
from gooddata_api_client.model.geo_json_feature_collection import GeoJsonFeatureCollection
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ogcapi_features_api.OGCAPIFeaturesApi(api_client)
    collection_id = "countries" # str | Collection identifier
    limit = 100 # int | Maximum number of features to return (optional)
    bbox = "-180,-90,180,90" # str | Bounding box filter (minx,miny,maxx,maxy) (optional)
    values = [
        "US,CA,MX",
    ] # [str] | List of values to filter features by (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get collection features
        api_response = api_instance.get_collection_items(collection_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OGCAPIFeaturesApi->get_collection_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get collection features
        api_response = api_instance.get_collection_items(collection_id, limit=limit, bbox=bbox, values=values)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OGCAPIFeaturesApi->get_collection_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Collection identifier |
 **limit** | **int**| Maximum number of features to return | [optional]
 **bbox** | **str**| Bounding box filter (minx,miny,maxx,maxy) | [optional]
 **values** | **[str]**| List of values to filter features by | [optional]

### Return type

[**GeoJsonFeatureCollection**](GeoJsonFeatureCollection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Features retrieved successfully |  -  |
**404** | Collection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

# **get_custom_collection_items**
> GeoJsonFeatureCollection get_custom_collection_items(collection_id)

Get custom collection features

Retrieve features from a custom (organization-scoped) GeoCollections collection as GeoJSON

### Example


```python
import time
import gooddata_api_client
from gooddata_api_client.api import ogcapi_features_api
from gooddata_api_client.model.geo_json_feature_collection import GeoJsonFeatureCollection
from pprint import pprint
# Defining the host is optional and defaults to http://localhost
# See configuration.py for a list of all supported configuration parameters.
configuration = gooddata_api_client.Configuration(
    host = "http://localhost"
)


# Enter a context with an instance of the API client
with gooddata_api_client.ApiClient() as api_client:
    # Create an instance of the API class
    api_instance = ogcapi_features_api.OGCAPIFeaturesApi(api_client)
    collection_id = "my-custom-collection" # str | Collection identifier
    limit = 100 # int | Maximum number of features to return (optional)
    bbox = "-180,-90,180,90" # str | Bounding box filter (minx,miny,maxx,maxy) (optional)
    values = [
        "US,CA,MX",
    ] # [str] | List of values to filter features by (optional)

    # example passing only required values which don't have defaults set
    try:
        # Get custom collection features
        api_response = api_instance.get_custom_collection_items(collection_id)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OGCAPIFeaturesApi->get_custom_collection_items: %s\n" % e)

    # example passing only required values which don't have defaults set
    # and optional values
    try:
        # Get custom collection features
        api_response = api_instance.get_custom_collection_items(collection_id, limit=limit, bbox=bbox, values=values)
        pprint(api_response)
    except gooddata_api_client.ApiException as e:
        print("Exception when calling OGCAPIFeaturesApi->get_custom_collection_items: %s\n" % e)
```


### Parameters

Name | Type | Description  | Notes
------------- | ------------- | ------------- | -------------
 **collection_id** | **str**| Collection identifier |
 **limit** | **int**| Maximum number of features to return | [optional]
 **bbox** | **str**| Bounding box filter (minx,miny,maxx,maxy) | [optional]
 **values** | **[str]**| List of values to filter features by | [optional]

### Return type

[**GeoJsonFeatureCollection**](GeoJsonFeatureCollection.md)

### Authorization

No authorization required

### HTTP request headers

 - **Content-Type**: Not defined
 - **Accept**: */*


### HTTP response details

| Status code | Description | Response headers |
|-------------|-------------|------------------|
**200** | Features retrieved successfully |  -  |
**404** | Collection not found |  -  |

[[Back to top]](#) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to Model list]](../README.md#documentation-for-models) [[Back to README]](../README.md)

