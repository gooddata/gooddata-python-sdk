# GrandTotal

Definition of a grand total. Grand total data will be computed into a separate section of the result structure so that client has more options how to visualize them.

## Properties
Name | Type | Description | Notes
------------ | ------------- | ------------- | -------------
**local_identifier** | **str** | Grand total identification within this request. The corresponding data in the result are expected to be matched using this identifier. | 
**function** | **str** | Aggregation function for grand total computation. | 
**included_dimensions** | [**{str: (IncludedDimensionProps,)}**](IncludedDimensionProps.md) | Mapping specifying dimensions on which this grand total will be computed. Dimensions are referenced via their localIdentifiers. Optionally one can specify also the values (properties) of the dimensions&#39; attributes (see &#x60;&#x60;&#x60;dimensionAttributesValues&#x60;&#x60;&#x60;). | 
**any string name** | **bool, date, datetime, dict, float, int, list, str, none_type** | any string name can be used but the value must be the correct type | [optional]

[[Back to Model list]](../README.md#documentation-for-models) [[Back to API list]](../README.md#documentation-for-api-endpoints) [[Back to README]](../README.md)


