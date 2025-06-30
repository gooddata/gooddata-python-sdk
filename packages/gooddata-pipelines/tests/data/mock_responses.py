# (C) 2025 GoodData Corporation

from typing import Any

WDF_VALID_PAYLOAD = {
    "data": [
        {
            "id": "expected_wdf_setting_id",
            "type": "workspaceDataFilterSetting",
            "attributes": {
                "title": "",
                "filterValues": ["expected", "wdf", "values"],
            },
            "relationships": {
                "workspaceDataFilter": {
                    "data": {
                        "id": "expected_wdf_id",
                        "type": "workspaceDataFilter",
                    },
                },
            },
            "links": {"self": "https://some.uri.com"},
            "meta": {
                "origin": {
                    "originType": "origin_type",
                    "originId": "origin_id",
                }
            },
        }
    ]
}

WDF_ACTUAL_WDF_SETTINGS: list[dict[str, Any]] = [
    {
        "id": "expected_wdf_setting_id",
        "type": "workspaceDataFilterSetting",
        "attributes": {
            "title": "",
            "filterValues": ["expected", "wdf", "values"],
        },
        "relationships": {
            "workspaceDataFilter": {
                "data": {
                    "id": "expected_wdf_id",
                    "type": "workspaceDataFilter",
                },
            },
        },
        "links": {"self": "https://some.uri.com"},
        "meta": {
            "origin": {
                "originType": "origin_type",
                "originId": "workspace_id",
            }
        },
    },
    {
        "id": "expected_wdf_setting_id_2",
        "type": "workspaceDataFilterSetting",
        "attributes": {
            "title": "",
            "filterValues": ["expected", "wdf", "values"],
        },
        "relationships": {
            "workspaceDataFilter": {
                "data": {
                    "id": "expected_wdf_id_2",
                    "type": "workspaceDataFilter",
                },
            },
        },
        "links": {"self": "https://some.uri.com"},
        "meta": {
            "origin": {
                "originType": "origin_type",
                "originId": "workspace_id",
            }
        },
    },
    # expected_wdf_id_3 is missing
    {
        "id": "expected_wdf_setting_id_4",
        "type": "workspaceDataFilterSetting",
        "attributes": {
            "title": "",
            "filterValues": ["expected", "wdf", "values"],
        },
        "relationships": {
            "workspaceDataFilter": {
                "data": {
                    "id": "expected_wdf_id_4",
                    "type": "workspaceDataFilter",
                },
            },
        },
        "links": {"self": "https://some.uri.com"},
        "meta": {
            "origin": {
                "originType": "origin_type",
                "originId": "workspace_id",
            }
        },
    },
]
