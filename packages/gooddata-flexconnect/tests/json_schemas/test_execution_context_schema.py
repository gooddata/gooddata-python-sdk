# (C) 2024 GoodData Corporation
import pytest
from jsonschema.exceptions import ValidationError


@pytest.mark.parametrize(
    "value",
    [
        # minimal valid schema for REPORT execution type
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
        },
        # REPORT with executionInitiator display
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
            "executionInitiator": {
                "type": "display",
                "dashboardId": "d1",
                "visualizationId": "v1",
                "widgetId": "w1",
            },
        },
        # REPORT with executionInitiator adhocExport
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
            "executionInitiator": {
                "type": "adhocExport",
                "dashboardId": "d1",
                "visualizationId": "v1",
                "widgetId": "w1",
                "exportType": "CSV",
            },
        },
        # REPORT with executionInitiator automation
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
            "executionInitiator": {
                "type": "automation",
                "automationId": "a1",
            },
        },
        # REPORT with executionInitiator alert
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
            "executionInitiator": {
                "type": "alert",
                "dashboardId": "d1",
                "visualizationId": "v1",
                "widgetId": "w1",
            },
        },
        # minimal valid schema for LABEL_ELEMENTS execution type
        {
            "executionType": "LABEL_ELEMENTS",
            "organizationId": "org2",
            "workspaceId": "ws2",
            "userId": "user2",
            "attributes": [],
            "filters": [],
            "labelElementsExecutionRequest": {"label": "label1"},
        },
        # full valid schema for LABEL_ELEMENTS execution type
        {
            "executionType": "LABEL_ELEMENTS",
            "organizationId": "org3",
            "workspaceId": "ws3",
            "userId": "user3",
            "timestamp": "2023-10-01T10:15:30+01:00",
            "timezone": "UTC",
            "week_start": "MONDAY",
            "attributes": [
                {
                    "attributeIdentifier": "attr1",
                    "attributeTitle": "Attribute 1",
                    "labelIdentifier": "label1",
                    "labelTitle": "Label 1",
                }
            ],
            "filters": [],
            "labelElementsExecutionRequest": {
                "label": "label2",
                "limit": 5,
                "offset": 2,
                "excludePrimaryLabel": False,
                "exactFilter": ["value3"],
                "patternFilter": "pattern?",
                "complementFilter": True,
                "dependsOn": [{"label": "parent1", "values": ["foo", "bar"]}],
                "validateBy": [{"id": "validator2", "type": "attribute"}],
            },
        },
    ],
)
def test_valid_execution_context_schema(value, get_validator):
    validator = get_validator("execution-context/execution-context.json")
    validator.validate(value)


@pytest.mark.parametrize(
    "value",
    [
        # missing required properties
        {"executionType": "REPORT"},
        {"organizationId": "org1"},
        {"workspaceId": "ws1"},
        {"userId": "user1"},
        {"attributes": []},
        {"filters": []},
        # invalid executionType
        {
            "executionType": "INVALID",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
        },
        # missing reportExecutionRequest for REPORT type
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
        },
        # missing labelElementsExecutionRequest for LABEL_ELEMENTS type
        {
            "executionType": "LABEL_ELEMENTS",
            "organizationId": "org2",
            "workspaceId": "ws2",
            "userId": "user2",
            "attributes": [],
            "filters": [],
        },
        # invalid attribute structure
        {
            "executionType": "LABEL_ELEMENTS",
            "organizationId": "org3",
            "workspaceId": "ws3",
            "userId": "user3",
            "attributes": [{"attributeIdentifier": "attr1"}],  # missing required properties
            "filters": [],
            "labelElementsExecutionRequest": {"label": "label2"},
        },
        # invalid executionInitiator type
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
            "executionInitiator": {
                "type": "INVALID",
            },
        },
        # automation initiator must not contain dashboardId
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
            "executionInitiator": {
                "type": "automation",
                "automationId": "a1",
                "dashboardId": "d1",
            },
        },
        # display initiator must not contain exportType
        {
            "executionType": "REPORT",
            "organizationId": "org1",
            "workspaceId": "ws1",
            "userId": "user1",
            "attributes": [],
            "filters": [],
            "reportExecutionRequest": {},
            "executionInitiator": {
                "type": "display",
                "dashboardId": "d1",
                "exportType": "CSV",
            },
        },
    ],
)
def test_invalid_execution_context_schema(value, get_validator):
    validator = get_validator("execution-context/execution-context.json")
    with pytest.raises(ValidationError):
        validator.validate(value)
