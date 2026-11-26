# (C) 2026 GoodData Corporation
"""Unit test: automation fields survive the declarative round trip."""

from __future__ import annotations

import pytest
from gooddata_sdk import CatalogDeclarativeAutomation, SlidesExportRequest

_AUTOMATION = {
    "id": "weekly-widgets",
    "title": "Weekly widgets",
    "evaluationMode": "PER_RECIPIENT",
    "analyticalDashboard": {"id": "sales", "type": "analyticalDashboard"},
    "externalRecipients": [{"email": "someone@example.com"}],
    "imageExports": [
        {
            "requestPayload": {
                "dashboardId": "sales",
                "fileName": "revenue",
                "format": "PNG",
                "widgetIds": ["revenue-widget"],
                "timezoneId": "Europe/Prague",
            }
        }
    ],
    "slidesExports": [
        {
            "requestPayload": {
                "dashboardId": "sales",
                "fileName": "sales",
                "format": "PPTX",
                "templateId": "branded",
                "widgetIds": ["revenue-widget"],
                "timezoneId": "Europe/Prague",
            }
        }
    ],
}


def test_automation_fields_survive_round_trip() -> None:
    automation = CatalogDeclarativeAutomation.from_dict(_AUTOMATION)

    assert automation.evaluation_mode == "PER_RECIPIENT"
    assert automation.analytical_dashboard is not None
    assert automation.analytical_dashboard.id == "sales"
    assert automation.external_recipients is not None
    assert automation.external_recipients[0].email == "someone@example.com"
    assert automation.image_exports is not None
    assert automation.image_exports[0].request_payload.widget_ids == ["revenue-widget"]
    assert automation.slides_exports is not None
    assert automation.slides_exports[0].request_payload.timezone_id == "Europe/Prague"
    assert automation.slides_exports[0].request_payload.template_id == "branded"

    assert automation.to_api().to_dict(camel_case=True) == _AUTOMATION


def test_slides_export_request_still_takes_template_id_in_camel_case() -> None:
    with pytest.deprecated_call():
        request = SlidesExportRequest(file_name="sales", format="PDF", templateId="branded")

    assert request.template_id == "branded"
    assert request.to_api().to_dict()["template_id"] == "branded"
