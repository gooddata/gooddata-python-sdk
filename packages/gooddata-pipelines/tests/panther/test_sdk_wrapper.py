# (C) 2025 GoodData Corporation

import pytest
from gooddata_api_client import ApiException  # type: ignore[import]
from gooddata_sdk.catalog.workspace.entity_model.workspace import (
    CatalogWorkspace,
)

from gooddata_pipelines.api.exceptions import GoodDataApiException
from gooddata_pipelines.api.utils import raise_with_context

GOODDATA_WRAPPER_OBJECT_PATH = (
    "gooddata_pipelines.api.gooddata_api_wrapper.GoodDataApi.list_workspaces"
)


def test_raise_with_context_reraises_panther_exception():
    @raise_with_context()
    def func():
        raise GoodDataApiException("Caught a GoodDataApiException")

    with pytest.raises(GoodDataApiException) as exc:
        func()
    assert "GoodDataApiException: Caught a GoodDataApiException" in str(
        exc.value
    )


def test_raise_with_context_wraps_generic_exception():
    @raise_with_context(api_endpoint="some.function.name")
    def func():
        raise ValueError("fail")

    with pytest.raises(GoodDataApiException) as exc:
        func()
        assert "ValueError: Some error: fail" in str(exc.value)
        assert exc.value.api_endpoint == "some.function.name"


def test_raise_with_context_wraps_apiexception_and_sets_error_template():
    @raise_with_context(api_endpoint="endpoint")
    def func():
        raise ApiException(404, "Not Found")

    with pytest.raises(GoodDataApiException) as exc:
        func()
        assert "ApiException: 404 Not Found" in str(exc.value)
        assert exc.value.api_endpoint == "endpoint"
        assert exc.value.http_status == "404 Not Found"


def test_raise_with_context_passes_method_kwargs():
    @raise_with_context()
    def func(**kwargs):
        raise RuntimeError("fail")

    with pytest.raises(GoodDataApiException) as exc:
        func(http_method="bar")
        assert exc.value.http_method == "bar"


def test_get_panther_children_workspaces_empty_response(
    mock_gooddata_api, mocker
) -> None:
    parent_ids: set[str] = {"parent_id_1", "parent_id_2"}

    mocker.patch(
        GOODDATA_WRAPPER_OBJECT_PATH,
        return_value=[],
    )

    panther_children = mock_gooddata_api.get_panther_children_workspaces(
        parent_ids
    )

    assert panther_children == []


def test_get_panther_children_full_match(mock_gooddata_api, mocker) -> None:
    parent_ids: set[str] = {"parent_id_1", "parent_id_2"}

    mocker.patch(
        GOODDATA_WRAPPER_OBJECT_PATH,
        return_value=[
            CatalogWorkspace(
                workspace_id="workspace_id1",
                name="workspace_title1",
                parent_id="parent_id_1",
            ),
            CatalogWorkspace(
                workspace_id="workspace_id2",
                name="workspace_title2",
                parent_id="parent_id_2",
            ),
        ],
    )

    panther_children = mock_gooddata_api.get_panther_children_workspaces(
        parent_ids
    )

    assert len(panther_children) == 2
    assert panther_children[0].workspace_id == "workspace_id1"
    assert panther_children[1].workspace_id == "workspace_id2"


def test_get_panther_children_no_match(mock_gooddata_api, mocker) -> None:
    parent_ids: set[str] = {"parent_id_3", "parent_id_4"}

    mocker.patch(
        GOODDATA_WRAPPER_OBJECT_PATH,
        return_value=[
            CatalogWorkspace(
                workspace_id="workspace_id1",
                name="workspace_title1",
                parent_id="parent_id_1",
            ),
            CatalogWorkspace(
                workspace_id="workspace_id2",
                name="workspace_title2",
                parent_id="parent_id_2",
            ),
        ],
    )

    panther_children = mock_gooddata_api.get_panther_children_workspaces(
        parent_ids
    )

    assert len(panther_children) == 0
