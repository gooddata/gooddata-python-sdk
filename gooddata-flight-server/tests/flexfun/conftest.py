# (C) 2024 GoodData Corporation
import pytest


@pytest.fixture
def sample_report_execution_context_dict():
    return {
        "execution_type": "REPORT",
        "organization_id": "default",
        "workspace_id": "646937086c794101984a7adf99a4854b",
        "user_id": "demo",
        "timestamp": "2024-09-12T12:51:26+00:00",
        "timezone": "Etc/UTC",
        "week_start": "sunday",
        "execution_request": {
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
        "report_execution_request": {
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
        "label_elements_execution_request": None,
        "attributes": [
            {
                "attribute_identifier": "attribute1",
                "attribute_title": "Attribute1",
                "label_identifier": "attribute1",
                "label_title": "Attribute1",
                "date_granularity": None,
                "sorting": None,
            }
        ],
        "filters": [{"filter_type": "negativeAttributeFilter", "label_identifier": "attribute1", "values": ["id1"]}],
    }


@pytest.fixture
def sample_label_execution_context_dict():
    return {
        "execution_type": "LABEL_ELEMENTS",
        "organization_id": "default",
        "workspace_id": "646937086c794101984a7adf99a4854b",
        "user_id": "demo",
        "timestamp": "",
        "timezone": "",
        "week_start": "sunday",
        "execution_request": {
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
        "report_execution_request": None,
        "label_elements_execution_request": {
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
                "attribute_identifier": "attribute2",
                "attribute_title": "Attribute2",
                "label_identifier": "attribute2",
                "label_title": "Attribute2",
                "date_granularity": None,
                "sorting": None,
            }
        ],
        "filters": [{"filter_type": "negativeAttributeFilter", "label_identifier": "attribute1", "values": ["id1"]}],
    }
