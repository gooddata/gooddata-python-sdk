# (C) 2024 GoodData Corporation
from gooddata_flexconnect.function.execution_context import (
    ExecutionContext,
    ExecutionContextAttribute,
    ExecutionContextNegativeAttributeFilter,
    ExecutionType,
)
from gooddata_sdk import (
    Attribute,
    CatalogDependsOn,
    CatalogFilterBy,
    CatalogValidateByItem,
    Metric,
    NegativeAttributeFilter,
)


def test_report_execution_context_deser(sample_report_execution_context_dict):
    """
    Test deserialization of the ExecutionContext object with the report execution request.
    Focus on checking that the result is populated with correct object types.
    """
    deserialized = ExecutionContext.from_dict(sample_report_execution_context_dict)

    assert deserialized.execution_type == ExecutionType.REPORT
    assert deserialized.organization_id == "default"
    assert deserialized.label_elements_execution_request is None

    assert deserialized.report_execution_request is not None
    assert isinstance(deserialized.report_execution_request.metrics[0], Metric)
    assert isinstance(deserialized.report_execution_request.attributes[0], Attribute)
    assert isinstance(deserialized.report_execution_request.filters[0], NegativeAttributeFilter)

    assert isinstance(deserialized.attributes[0], ExecutionContextAttribute)
    assert isinstance(deserialized.filters[0], ExecutionContextNegativeAttributeFilter)


def test_label_elements_execution_context_deser(sample_label_execution_context_dict):
    """
    Test deserialization of the ExecutionContext object with the label elements execution request.
    Focus on checking that the result is populated with correct object types.
    """
    deserialized = ExecutionContext.from_dict(sample_label_execution_context_dict)

    assert deserialized.execution_type == ExecutionType.LABEL_ELEMENTS
    assert deserialized.organization_id == "default"
    assert deserialized.report_execution_request is None

    assert deserialized.label_elements_execution_request is not None
    assert isinstance(deserialized.label_elements_execution_request.filter_by, CatalogFilterBy)
    assert deserialized.label_elements_execution_request.filter_by.label_type == "REQUESTED"
    assert isinstance(deserialized.label_elements_execution_request.depends_on[0], CatalogDependsOn)
    assert isinstance(deserialized.label_elements_execution_request.validate_by[0], CatalogValidateByItem)

    assert isinstance(deserialized.attributes[0], ExecutionContextAttribute)
    assert isinstance(deserialized.filters[0], ExecutionContextNegativeAttributeFilter)
