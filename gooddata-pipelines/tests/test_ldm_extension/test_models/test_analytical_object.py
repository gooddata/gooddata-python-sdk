# (C) 2025 GoodData Corporation
import orjson
import pytest

from gooddata_pipelines.ldm_extension.models.analytical_object import (
    AnalyticalObject,
    AnalyticalObjects,
)
from tests.conftest import TEST_DATA_DIR


@pytest.mark.parametrize(
    "file_path",
    [
        f"{TEST_DATA_DIR}/custom_fields/response_get_all_metrics.json",
        f"{TEST_DATA_DIR}/custom_fields/response_get_all_visualizations.json",
        f"{TEST_DATA_DIR}/custom_fields/response_get_all_dashboards.json",
    ],
)
def test_analytical_object_model_with_metrics(file_path):
    with open(file_path, "r") as file:
        data = orjson.loads(file.read())
    analytical_objects = AnalyticalObjects(**data)
    assert isinstance(analytical_objects, AnalyticalObjects)
    assert isinstance(analytical_objects.data, list)
    assert all(
        isinstance(obj, AnalyticalObject) for obj in analytical_objects.data
    )


@pytest.mark.parametrize(
    "response",
    [
        {
            "something": "unexpected",
        },
        {
            "data": [
                {
                    # "id": "metric1", # Missing id field
                    "type": "metric",
                    "attributes": {
                        "title": "Test Metric",
                        "areRelationsValid": True,
                    },
                }
            ]
        },
        {
            "data": [
                {
                    "id": 123,  # invalid id type
                    "type": "metric",
                    "attributes": {
                        "title": "Test Metric",
                        "areRelationsValid": True,
                    },
                }
            ]
        },
    ],
)
def test_analytical_object_model_with_invalid_response(response):
    with pytest.raises(ValueError):
        AnalyticalObjects(**response)
