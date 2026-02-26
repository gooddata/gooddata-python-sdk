# (C) 2024 GoodData Corporation
import pytest

from gooddata_flexconnect.function.execution_context import (
    ExecutionContext,
    ExecutionContextAttribute,
    ExecutionContextNegativeAttributeFilter,
    ExecutionInitiatorAdHocExport,
    ExecutionInitiatorAlert,
    ExecutionInitiatorAutomation,
    ExecutionInitiatorDisplay,
    ExecutionType,
    _dict_to_execution_initiator,
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

    assert deserialized is not None
    assert deserialized.execution_type == ExecutionType.REPORT
    assert deserialized.organization_id == "default"
    assert deserialized.label_elements_execution_request is None

    assert deserialized.report_execution_request is not None
    assert isinstance(deserialized.report_execution_request.metrics[0], Metric)
    assert isinstance(deserialized.report_execution_request.attributes[0], Attribute)
    assert isinstance(deserialized.report_execution_request.filters[0], NegativeAttributeFilter)

    assert isinstance(deserialized.attributes[0], ExecutionContextAttribute)
    assert isinstance(deserialized.filters[0], ExecutionContextNegativeAttributeFilter)

    assert deserialized.execution_initiator is not None
    assert isinstance(deserialized.execution_initiator, ExecutionInitiatorDisplay)
    assert deserialized.execution_initiator.dashboard_id == "b2f2d436-9831-4fe0-81df-8c59fd33242b"
    assert deserialized.execution_initiator.visualization_id == "bf21d8ec-742c-48d7-8100-80663b43622b"
    assert deserialized.execution_initiator.widget_id == "453844a7-4aa8-4456-be23-ac62b9b3b98a"


def test_label_elements_execution_context_deser(sample_label_execution_context_dict):
    """
    Test deserialization of the ExecutionContext object with the label elements execution request.
    Focus on checking that the result is populated with correct object types.
    """
    deserialized = ExecutionContext.from_dict(sample_label_execution_context_dict)

    assert deserialized is not None
    assert deserialized.execution_type == ExecutionType.LABEL_ELEMENTS
    assert deserialized.organization_id == "default"
    assert deserialized.report_execution_request is None

    assert deserialized.label_elements_execution_request is not None
    assert isinstance(deserialized.label_elements_execution_request.filter_by, CatalogFilterBy)
    assert deserialized.label_elements_execution_request.filter_by.label_type == "REQUESTED"
    assert deserialized.label_elements_execution_request.depends_on is not None
    assert isinstance(deserialized.label_elements_execution_request.depends_on[0], CatalogDependsOn)
    assert deserialized.label_elements_execution_request.validate_by is not None
    assert isinstance(deserialized.label_elements_execution_request.validate_by[0], CatalogValidateByItem)

    assert isinstance(deserialized.attributes[0], ExecutionContextAttribute)
    assert isinstance(deserialized.filters[0], ExecutionContextNegativeAttributeFilter)

    assert deserialized.execution_initiator is None


@pytest.mark.parametrize(
    "initiator_dict, expected_type",
    [
        (
            {
                "type": "display",
                "dashboardId": "d1",
                "visualizationId": "v1",
                "widgetId": "w1",
            },
            ExecutionInitiatorDisplay,
        ),
        (
            {
                "type": "adhocExport",
                "dashboardId": "d1",
                "visualizationId": "v1",
                "widgetId": "w1",
                "exportType": "CSV",
            },
            ExecutionInitiatorAdHocExport,
        ),
        (
            {
                "type": "automation",
                "automationId": "a1",
            },
            ExecutionInitiatorAutomation,
        ),
        (
            {
                "type": "alert",
                "dashboardId": "d1",
                "visualizationId": "v1",
                "widgetId": "w1",
            },
            ExecutionInitiatorAlert,
        ),
    ],
    ids=["display", "adhocExport", "automation", "alert"],
)
def test_execution_initiator_deser(initiator_dict, expected_type):
    result = _dict_to_execution_initiator(initiator_dict)
    assert isinstance(result, expected_type)


def test_execution_initiator_unknown_type():
    with pytest.raises(ValueError, match="Unsupported execution initiator type"):
        _dict_to_execution_initiator({"type": "unknown"})
