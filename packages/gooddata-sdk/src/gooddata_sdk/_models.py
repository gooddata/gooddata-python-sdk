# (C) 2025 GoodData Corporation
"""Direct imports of the generated API models used by the SDK.

``gooddata_api_client.models`` eagerly imports all ~1400 generated model classes, of which
the SDK uses only the few dozen re-exported here. Importing the leaf modules instead keeps
``import gooddata_sdk`` cheap. Keep this list in sync with the models the SDK references.
"""

from gooddata_api_client.model.absolute_date_filter import AbsoluteDateFilter
from gooddata_api_client.model.afm import AFM
from gooddata_api_client.model.afm_execution import AfmExecution
from gooddata_api_client.model.afm_execution_response import AfmExecutionResponse
from gooddata_api_client.model.afm_identifier import AfmIdentifier
from gooddata_api_client.model.afm_local_identifier import AfmLocalIdentifier
from gooddata_api_client.model.afm_object_identifier import AfmObjectIdentifier
from gooddata_api_client.model.afm_object_identifier_attribute import AfmObjectIdentifierAttribute
from gooddata_api_client.model.afm_object_identifier_attribute_identifier import AfmObjectIdentifierAttributeIdentifier
from gooddata_api_client.model.afm_object_identifier_dataset import AfmObjectIdentifierDataset
from gooddata_api_client.model.afm_object_identifier_dataset_identifier import AfmObjectIdentifierDatasetIdentifier
from gooddata_api_client.model.afm_object_identifier_identifier import AfmObjectIdentifierIdentifier
from gooddata_api_client.model.afm_object_identifier_label import AfmObjectIdentifierLabel
from gooddata_api_client.model.afm_object_identifier_label_identifier import AfmObjectIdentifierLabelIdentifier
from gooddata_api_client.model.afm_valid_objects_query import AfmValidObjectsQuery
from gooddata_api_client.model.all_time_date_filter import AllTimeDateFilter
from gooddata_api_client.model.arithmetic_measure_definition import ArithmeticMeasureDefinition
from gooddata_api_client.model.arithmetic_measure_definition_arithmetic_measure import (
    ArithmeticMeasureDefinitionArithmeticMeasure,
)
from gooddata_api_client.model.attribute_filter_elements import AttributeFilterElements
from gooddata_api_client.model.attribute_item import AttributeItem
from gooddata_api_client.model.bounded_filter import BoundedFilter
from gooddata_api_client.model.comparison_condition_comparison import ComparisonConditionComparison
from gooddata_api_client.model.comparison_measure_value_filter import ComparisonMeasureValueFilter
from gooddata_api_client.model.compound_measure_value_filter import CompoundMeasureValueFilter
from gooddata_api_client.model.dimension import Dimension
from gooddata_api_client.model.dimension_header import DimensionHeader
from gooddata_api_client.model.execution_response import ExecutionResponse
from gooddata_api_client.model.execution_result import ExecutionResult
from gooddata_api_client.model.execution_result_grand_total import ExecutionResultGrandTotal
from gooddata_api_client.model.execution_result_metadata import ExecutionResultMetadata
from gooddata_api_client.model.execution_result_paging import ExecutionResultPaging
from gooddata_api_client.model.inline_filter_definition import InlineFilterDefinition
from gooddata_api_client.model.inline_measure_definition import InlineMeasureDefinition
from gooddata_api_client.model.inline_measure_definition_inline import InlineMeasureDefinitionInline
from gooddata_api_client.model.match_attribute_filter import MatchAttributeFilter
from gooddata_api_client.model.measure_item import MeasureItem
from gooddata_api_client.model.measure_value_condition import MeasureValueCondition
from gooddata_api_client.model.negative_attribute_filter import NegativeAttributeFilter
from gooddata_api_client.model.pop_dataset import PopDataset
from gooddata_api_client.model.pop_dataset_measure_definition import PopDatasetMeasureDefinition
from gooddata_api_client.model.pop_dataset_measure_definition_previous_period_measure import (
    PopDatasetMeasureDefinitionPreviousPeriodMeasure,
)
from gooddata_api_client.model.pop_date import PopDate
from gooddata_api_client.model.pop_date_measure_definition import PopDateMeasureDefinition
from gooddata_api_client.model.pop_date_measure_definition_over_period_measure import (
    PopDateMeasureDefinitionOverPeriodMeasure,
)
from gooddata_api_client.model.positive_attribute_filter import PositiveAttributeFilter
from gooddata_api_client.model.range_condition_range import RangeConditionRange
from gooddata_api_client.model.range_measure_value_filter import RangeMeasureValueFilter
from gooddata_api_client.model.ranking_filter import RankingFilter
from gooddata_api_client.model.relative_date_filter import RelativeDateFilter
from gooddata_api_client.model.result_cache_metadata import ResultCacheMetadata
from gooddata_api_client.model.result_spec import ResultSpec
from gooddata_api_client.model.simple_measure_definition import SimpleMeasureDefinition
from gooddata_api_client.model.simple_measure_definition_measure import SimpleMeasureDefinitionMeasure
from gooddata_api_client.model.sort_key import SortKey
from gooddata_api_client.model.sort_key_attribute_attribute import SortKeyAttributeAttribute
from gooddata_api_client.model.sort_key_value_value import SortKeyValueValue
from gooddata_api_client.model.total import Total
from gooddata_api_client.model.total_dimension import TotalDimension

__all__ = [
    "AFM",
    "AbsoluteDateFilter",
    "AfmExecution",
    "AfmExecutionResponse",
    "AfmIdentifier",
    "AfmLocalIdentifier",
    "AfmObjectIdentifier",
    "AfmObjectIdentifierAttribute",
    "AfmObjectIdentifierAttributeIdentifier",
    "AfmObjectIdentifierDataset",
    "AfmObjectIdentifierDatasetIdentifier",
    "AfmObjectIdentifierIdentifier",
    "AfmObjectIdentifierLabel",
    "AfmObjectIdentifierLabelIdentifier",
    "AfmValidObjectsQuery",
    "AllTimeDateFilter",
    "ArithmeticMeasureDefinition",
    "ArithmeticMeasureDefinitionArithmeticMeasure",
    "AttributeFilterElements",
    "AttributeItem",
    "BoundedFilter",
    "ComparisonConditionComparison",
    "ComparisonMeasureValueFilter",
    "CompoundMeasureValueFilter",
    "Dimension",
    "DimensionHeader",
    "ExecutionResponse",
    "ExecutionResult",
    "ExecutionResultGrandTotal",
    "ExecutionResultMetadata",
    "ExecutionResultPaging",
    "InlineFilterDefinition",
    "InlineMeasureDefinition",
    "InlineMeasureDefinitionInline",
    "MatchAttributeFilter",
    "MeasureItem",
    "MeasureValueCondition",
    "NegativeAttributeFilter",
    "PopDataset",
    "PopDatasetMeasureDefinition",
    "PopDatasetMeasureDefinitionPreviousPeriodMeasure",
    "PopDate",
    "PopDateMeasureDefinition",
    "PopDateMeasureDefinitionOverPeriodMeasure",
    "PositiveAttributeFilter",
    "RangeConditionRange",
    "RangeMeasureValueFilter",
    "RankingFilter",
    "RelativeDateFilter",
    "ResultCacheMetadata",
    "ResultSpec",
    "SimpleMeasureDefinition",
    "SimpleMeasureDefinitionMeasure",
    "SortKey",
    "SortKeyAttributeAttribute",
    "SortKeyValueValue",
    "Total",
    "TotalDimension",
]
