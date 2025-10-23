# (C) 2024 GoodData Corporation
import pytest


@pytest.fixture
def sample_report_execution_context_dict():
    return {
        "executionType": "REPORT",
        "organizationId": "default",
        "workspaceId": "646937086c794101984a7adf99a4854b",
        "userId": "demo",
        "timestamp": "2024-09-12T12:51:26+00:00",
        "timezone": "Etc/UTC",
        "weekStart": "sunday",
        "executionRequest": {
            "attributes": [
                {
                    "localIdentifier": "a_attribute1",
                    "label": {"identifier": {"id": "attribute1", "type": "label"}},
                    "showAllValues": False,
                }
            ],
            "filters": [
                {
                    "negativeAttributeFilter": {
                        "label": {"identifier": {"id": "attribute1", "type": "label"}},
                        "notIn": {"values": ["id1"]},
                        "applyOnResult": None,
                    }
                }
            ],
            "measures": [
                {
                    "localIdentifier": "m_fact1_min",
                    "definition": {
                        "measure": {
                            "item": {"identifier": {"id": "fact1", "type": "fact"}},
                            "aggregation": "MIN",
                            "computeRatio": False,
                            "filters": [],
                        }
                    },
                }
            ],
            "auxMeasures": [],
        },
        "reportExecutionRequest": {
            "attributes": [
                {
                    "localIdentifier": "a_attribute1",
                    "label": {"identifier": {"id": "attribute1", "type": "label"}},
                    "showAllValues": False,
                }
            ],
            "filters": [
                {
                    "negativeAttributeFilter": {
                        "label": {"identifier": {"id": "attribute1", "type": "label"}},
                        "notIn": {"values": ["id1"]},
                        "applyOnResult": None,
                    }
                }
            ],
            "measures": [
                {
                    "localIdentifier": "m_fact1_min",
                    "definition": {
                        "measure": {
                            "item": {"identifier": {"id": "fact1", "type": "fact"}},
                            "aggregation": "MIN",
                            "computeRatio": False,
                            "filters": [],
                        }
                    },
                }
            ],
            "auxMeasures": [],
        },
        "labelElementsExecutionRequest": None,
        "attributes": [
            {
                "attributeIdentifier": "attribute1",
                "attributeTitle": "Attribute1",
                "labelIdentifier": "attribute1",
                "labelTitle": "Attribute1",
                "dateGranularity": None,
                "sorting": None,
            }
        ],
        "filters": [{"filterType": "negativeAttributeFilter", "labelIdentifier": "attribute1", "values": ["id1"]}],
    }


@pytest.fixture
def sample_label_execution_context_dict():
    return {
        "executionType": "LABEL_ELEMENTS",
        "organizationId": "default",
        "workspaceId": "646937086c794101984a7adf99a4854b",
        "userId": "demo",
        "timestamp": "",
        "timezone": "",
        "weekStart": "sunday",
        "executionRequest": {
            "attributes": [
                {
                    "localIdentifier": "label",
                    "label": {"identifier": {"id": "attribute2", "type": "label"}},
                    "showAllValues": False,
                }
            ],
            "filters": [
                {
                    "negativeAttributeFilter": {
                        "label": {"identifier": {"id": "attribute1", "type": "label"}},
                        "notIn": {"values": ["id1"]},
                        "applyOnResult": None,
                    }
                }
            ],
            "measures": [
                {
                    "localIdentifier": "fact1",
                    "definition": {
                        "measure": {
                            "item": {"identifier": {"id": "fact1", "type": "fact"}},
                            "aggregation": "SUM",
                            "computeRatio": False,
                            "filters": [],
                        }
                    },
                }
            ],
            "auxMeasures": [],
        },
        "reportExecutionRequest": None,
        "labelElementsExecutionRequest": {
            "label": "attribute2",
            "excludePrimaryLabel": True,
            "filterBy": {"labelType": "REQUESTED"},
            "complementFilter": False,
            "patternFilter": "search",
            "offset": 0,
            "limit": 500,
            "dependsOn": [{"label": "attribute1", "values": ["id1"], "complementFilter": True}],
            "validateBy": [{"id": "fact1", "type": "fact"}],
        },
        "attributes": [
            {
                "attributeIdentifier": "attribute2",
                "attributeTitle": "Attribute2",
                "labelIdentifier": "attribute2",
                "labelTitle": "Attribute2",
                "dateGranularity": None,
                "sorting": None,
            }
        ],
        "filters": [{"filterType": "negativeAttributeFilter", "labelIdentifier": "attribute1", "values": ["id1"]}],
    }
